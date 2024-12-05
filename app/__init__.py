from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import inspect

def create_app():
    app = Flask(__name__, static_folder="static")
    CORS(app, origins=["https://front-arquetipo-856517455627.europe-southwest1.run.app"],
         expose_headers=['Content-Type'], 
         supports_credentials=True)
    
    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.crud import crud_bp  # Import the new CRUD blueprint
    from app.routes.google_api_login import login_bp
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(crud_bp, url_prefix='/api')  # Register the CRUD blueprint
    app.register_blueprint(login_bp, url_prefix="/api")

    @app.route('/swagger.json')
    def swagger_json():
        return jsonify(generate_swagger(app))
    
    # Swagger UI setup
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'  # path to your API docs
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Flask API", 'lang': "en"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # After request function to enforce Content-Language
    @app.after_request
    def after_request(response):
        response.headers["Content-Language"] = "en"  # Force the Content-Language to English
        return response

    return app

def extract_routes(app):
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('swagger') or 'static' in rule.endpoint:
            continue
        handler = app.view_functions[rule.endpoint]
        doc = inspect.getdoc(handler) or "No documentation available"
        routes.append({
            "rule": rule.rule,
            "methods": list(rule.methods - {"HEAD", "OPTIONS"}),
            "doc": doc,
        })
    return routes

def generate_swagger(app):
    routes = extract_routes(app)
    swagger_schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Dynamic Flask API",
            "version": "1.0.0",
        },
        "paths": {}
    }
    for route in routes:
        swagger_schema["paths"][route["rule"]] = {
            method.lower(): {
                "summary": route["doc"],
                "responses": {
                    "200": {"description": "Success"}
                }
            } for method in route["methods"]
        }
    return swagger_schema