from FASTAflow import flask_app

if __name__ == '__main__':
    app = flask_app.create_app()
    app.run(port=8000)