from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

# Instantiate the extensions here but initialize them in create_app
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)  # Initialize the database extension
    bcrypt.init_app(app)  # Initialize Bcrypt
    login_manager.init_app(app)  # Initialize LoginManager
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Enable CORS

    # Register blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    return app