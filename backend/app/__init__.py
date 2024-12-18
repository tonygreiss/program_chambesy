from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Enable CORS with frontend domain
    CORS(app, origins=[os.environ.get('FRONTEND_URL', 'http://localhost:3000')], 
         supports_credentials=True)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app 