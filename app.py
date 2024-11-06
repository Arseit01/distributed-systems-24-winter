from flask import Flask, render_template, render_template_string
from flask_smorest import Api, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import markdown
import json
from flask_sqlalchemy import SQLAlchemy

# App and API Configurations
app = Flask(__name__)
app.config["API_TITLE"] = "Shopping API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"  # JSON endpoint for Swagger UI
app.config["OPENAPI_URL_PREFIX"] = "/"            # Serve OpenAPI JSON at the root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# Initialize database and API
db = SQLAlchemy(app)
api = Api(app)

# Define Blueprint with flask-smorest
blp = Blueprint("shopping", __name__, description="Operations on shopping items")

# Test data model
class Item(db.Model):
    name = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)

# Endpoint in Blueprint
@blp.route("/api/shopping/<string:name>")
@blp.response(200, description="Successfully retrieved item.")
def get_item(name):
    return {"name": name, "amount": 5}

# Register blueprint with the API
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
