"""Root package."""

import os
from flask_api import FlaskAPI
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine



DB = SQLAlchemy()

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.session_protection = 'strong'

BCRYPT = Bcrypt()

def create_app(config_type):
    """App factory.

    Args:
        config_type: Name of the config file without extension.
    Returns:
        App object.
    """
    # Create app with specified configuration.
    app = FlaskAPI(__name__)
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.abspath(os.path.join(curr_dir, os.pardir))

    configuration = os.path.join(root_dir, 'config', config_type + '.py')
    app.config.from_pyfile(configuration)
    app.config['SECRET_KEY'] = 'super secret key'
    # Initialize extensions for current app.
    DB.init_app(app)
    LOGIN_MANAGER.init_app(app)
    BCRYPT.init_app(app)
    CORS(app, supports_credentials=True)
    SSLify(app, skips=['health_check'])
    # Import and register blueprints.
    from app.auth import authentication
    from app.server import server
    app.register_blueprint(authentication)
    app.register_blueprint(server)
    return app
