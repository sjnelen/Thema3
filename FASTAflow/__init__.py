"""
The main part of the flask web application
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from flask import Flask

from FASTAflow import pages

def create_app():
    webapp = Flask(__name__)

    webapp.register_blueprint(pages.bp)
    return webapp

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
