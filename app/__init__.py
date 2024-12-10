from flask import Flask, jsonify
from flask_smorest import Api, Blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["API_TITLE"] = "Flask API"
    app.config["API_VERSION"] = "1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "swagger.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    CORS(app, origins=["https://front-arquetipo-856517455627.europe-southwest1.run.app"],
         expose_headers=['Content-Type'], 
         supports_credentials=True)
    api = Api(app)

    # Create a blueprint for your API
    blp = Blueprint("example", "example", url_prefix="/api", description="Example operations")

    @blp.route("/hello")
    @blp.doc(description="Returns a simple hello message.")
    def hello():
        """Returns a hello world message."""
        return jsonify({"message": "Hello, world!"})

    @blp.route("/add")
    @blp.doc(description="Adds two numbers.")
    @blp.arguments(
        {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number."},
                "b": {"type": "number", "description": "The second number."},
            },
            "required": ["a", "b"],
        },
        location="json",
    )
    @blp.response(200, {"result": {"type": "number"}}, description="The sum of the two numbers.")
    def add_numbers(data):
        """Adds two numbers and returns the result."""
        return jsonify({"result": data["a"] + data["b"]})

    # Register the blueprint
    api.register_blueprint(blp)
    return app
