from flask import Flask, render_template, render_template_string, send_from_directory
from flask_smorest import Api, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import markdown
import json

# App and API Configurations
app = Flask(__name__)
app.config["API_TITLE"] = "Shopping API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"  # Ensures flask-smorest generates the JSON

# Initialize flask-smorest API
api = Api(app)

# Read OpenAPI JSON for Swagger UI
@app.route("/openapi.json")
def serve_openapi_json():
    return send_from_directory('.', "rest_api.json")

# Set up Swagger UI
SWAGGER_URL = "/swagger"
API_URL = "/openapi.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "Shopping API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Define Blueprint with flask-smorest
blp = Blueprint("shopping", __name__, description="Operations on shopping items")

@blp.route("/api/shopping/<string:name>")
@blp.response(200, description="Successfully retrieved item.")
def get_item(name):
    return {"name": name, "amount": 5}

api.register_blueprint(blp)

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
