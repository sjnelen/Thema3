"""
This module initializes and configures the FASTAflow Flask application.

It defines a factory function that creates and configures the Flask application,
initializes the database connection, and sets up necessary components like blueprints.
"""
import os
from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

from FASTAflow import __version__
from FASTAflow.modules.models import db
from FASTAflow.modules import pages
from FASTAflow.config import DevelopmentConfig, ProductionConfig


def create_app(config_object=None):
    """Creates and configures the Flask application.

    Creates a new Flask application instance, configures the database connection,
    and initializes tables.

    Returns:
        Flask: A configured Flask application.

    Raises:
        OSError: If database directory creation fails.
    """
    app = Flask(__name__, static_folder='static')

    # Configure the application which defaults to DevelopmentConfig
    if config_object is None:
        config_object = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig
    app.config.from_object(config_object)

    # Make sure the required directories exist
    Path(app.config['DATABASE_DIR']).mkdir(parents=True, exist_ok=True)
    Path(app.config['UPLOAD_DIR']).mkdir(parents=True, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(pages.bp)

    # Configure middleware
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Handle proxy headers

    # Add version info into template context for every html template
    @app.context_processor
    def inject_version():
        return dict(version=__version__)

    # Initialize database
    with app.app_context():
        if app.config['DEBUG']:
            db.drop_all()  # Only in development
        db.create_all()
        app.logger.info(f"Database initialized at {app.config['SQLALCHEMY_DATABASE_URI']}")

    return app