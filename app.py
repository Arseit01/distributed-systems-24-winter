from flask import Flask, jsonify, render_template_string
from flask_smorest import Api, Blueprint, abort
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import markdown
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os
# App and API Configurations
app = Flask(__name__)
app.config["API_TITLE"] = "Shopping API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"  # JSON endpoint for Swagger UI
app.config["OPENAPI_URL_PREFIX"] = "/"            # Serve OpenAPI JSON at the root
db_path = os.path.join(os.path.dirname(__file__), "shopping.db")
#app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/shopping_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and API
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

# Define Blueprint with flask-smorest

class Item(db.Model):
    __tablename__ = "items"
    name = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)
    
    def serialize(self):
        return {
            "name": self.name,
            "amount": self.amount
        }
    
    

class ItemSchema(Schema):
    name = fields.String(required=True)
    amount = fields.Integer(required=True)

# Blueprint for shopping endpoints
blp = Blueprint("shopping", __name__, description="Operations on shopping items")

# Registering the schema
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Initialize the database
with app.app_context():
    db.create_all()

# Create a new item
@blp.route("/api/shopping", methods=["POST"])
@blp.arguments(ItemSchema)
@blp.response(201, ItemSchema)
def create_item(data):
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return item

# Get all items
@blp.route("/api/shopping", methods=["GET"])
@blp.response(200, ItemSchema(many=True))
def get_items():
    items = Item.query.all()
    return items

# Get an item by name
@blp.route("/api/shopping/<string:name>", methods=["GET"])
@blp.response(200, ItemSchema)
def get_item(name):
    try:
        item = Item.query.get_or_404(name)
        return jsonify({
            "message": "Item found and retrieved successfully.",
            "item": item.serialize()  # assuming `serialize()` converts `item` to a dictionary
        })
    except Exception as e:
        print(e)
        print("Exception got thrown")
        abort(404, message={"error": "Item not found", "item_name": name, "status": "fail"})

# Update an item by name
@blp.route("/api/shopping/<string:name>", methods=["PUT"])
@blp.arguments(ItemSchema)
@blp.response(200, ItemSchema)
def update_item(data, name):
    item = Item.query.get_or_404(name)
    item.amount = data["amount"]
    db.session.commit()
    return item

# Delete an item by name
@blp.route("/api/shopping/<string:name>", methods=["DELETE"])
@blp.response(204)
def delete_item(name):
    item = Item.query.get_or_404(name)
    db.session.delete(item)
    db.session.commit()
    return "", 204

# Register the blueprint with the API only once
api.register_blueprint(blp)

# Swagger UI configuration
SWAGGER_URL = "/swagger"
API_URL = f"/{app.config['OPENAPI_JSON_PATH']}"  # Should match openapi.json endpoint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Shopping API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Markdown rendering route
@app.route('/md')
def servemd():
    with open("README.md") as md_file:
        md_content = md_file.read()
        html_content = markdown.markdown(md_content)
        return render_template_string('<html><body>{{ content | safe }}</body></html>', content=html_content)

# Simple test route
@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
