from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Enable CORS with a simpler configuration
    CORS(app, supports_credentials=True)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app 