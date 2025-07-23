# app/__init__.py

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions without an app
db = SQLAlchemy()
socketio = SocketIO()
login = LoginManager()
# This tells Flask-Login where to redirect users if they try to access a protected page
login.login_view = 'main.login' 

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    # Configure your app. You should use a more secure way to set the secret key.
    # For a chat app with a database, you also need to configure the database URI.
    app.config['SECRET_KEY'] = 'a_very_secret_key!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db' # Example using SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    socketio.init_app(app)
    login.init_app(app)

    # Import the Blueprint from routes.py
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Import socketio events to register them
    from . import socketio_events

    # Import models so that they are known to SQLAlchemy
    from . import models

    return app