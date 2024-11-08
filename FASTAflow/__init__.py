"""
The main part of the flask web application
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

import os
import secrets

from flask import Flask

from FASTAflow.models import db
from FASTAflow import pages


def create_app():
    webapp = Flask(__name__)

    # Create a 'database' directory in your project root
    db_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
    os.makedirs(db_folder, exist_ok=True)

    db_path = os.path.join(db_folder, 'fastaflow.db')
    webapp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(webapp)

    with webapp.app_context():
        db.drop_all()
        db.create_all()
        print(f'database created at {db_path}')

    webapp.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
    webapp.register_blueprint(pages.bp)
    return webapp

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
