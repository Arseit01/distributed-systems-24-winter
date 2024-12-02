import os
from flask import Flask, jsonify, render_template_string
from flask_smorest import Api, Blueprint, abort
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import markdown
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask_migrate import Migrate
import psycopg2
import logging

from sqlalchemy.sql import text

# Load environment variables from .env file


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# App and API Configurations
app = Flask(__name__)
app.config["API_TITLE"] = "Shopping API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"
app.config["OPENAPI_URL_PREFIX"] = "/"

# Database configuration


db_path = os.path.join(os.path.dirname(__file__), "shopping.db")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database, API, CORS, and Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# Define database model
class Item(db.Model):
    __tablename__ = "items"
    name = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)

    def serialize(self):
        return {"name": self.name, "amount": self.amount}


# Schema for validation
class ItemSchema(Schema):
    name = fields.String(required=True)
    amount = fields.Integer(required=True)


# Blueprint for shopping endpoints
blp = Blueprint("shopping", __name__, description="Operations on shopping items")
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

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
    item = Item.query.get_or_404(name)
    return item


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


# Register the blueprint with the API
api.register_blueprint(blp)

# Swagger UI configuration
SWAGGER_URL = "/swagger"
API_URL = f"/{app.config['OPENAPI_JSON_PATH']}"
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


# Route to test database connection
@app.route('/db', methods=['GET'])
def test_db_connection_route():
    try:
        # Attempt to create a database session
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return jsonify({"success": True, "message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Database connection failed: {e}"}), 500



def test_db_connection():
    try:
        # Use SQLAlchemy engine to execute a simple query
        with db.engine.connect() as connection:
            result = connection.execute("SELECT 1").scalar()
            if result == 1:
                logging.info("Database connection successful!")
            else:
                logging.error("Unexpected result from database connection test.")
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise


# Main entry point
if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]
    db.create_all()
    
    try:
        test_db_connection()  # Test the database connection
    except Exception as e:
        logging.critical("Exiting application due to database connection failure.")
    app.run(debug=debug_mode, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
