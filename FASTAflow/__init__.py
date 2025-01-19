"""
This module initializes and configures the FASTAflow Flask application.

It defines a factory function that creates and configures the Flask application,
initializes the database connection, and sets up necessary components like blueprints.
"""

__author__ = 'Sam Nelen'
__version__ = '2025.01.16'

import os

from flask import Flask

from .models import db
import pages


def create_app():
    """Creates and configures the Flask application.

    Creates a new Flask application instance, configures the database connection,
    and initializes tables.

    Returns:
        Flask: A configured Flask application.

    Raises:
        OSError: If database directory creation fails.
    """
    webapp = Flask(__name__, static_folder='static')

    # Create a 'database' directory in your project root
    db_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
    os.makedirs(db_folder, exist_ok=True)

    db_path = os.path.join(db_folder, 'fastaflow.db')
    webapp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    webapp.secret_key = 'z\x16_\x0f\xe2N\xdd\x83^\x07!<'

    db.init_app(webapp)

    with webapp.app_context():
        db.drop_all()
        db.create_all()
        print(f'database created at {db_path}')

    webapp.register_blueprint(pages.bp)
    return webapp

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
