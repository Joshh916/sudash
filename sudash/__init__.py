from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .servarr_connectors import stall_manager
import threading

# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    t = threading.Thread(target=stall_manager.start_stall_schedule)
    t.start()
    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    print(os.getcwd())

    with app.app_context():
        # Include our Routes
        from . import routes
        from . import auth

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        db.create_all()

        return app