import os

from flask import Flask


# app factory
def create_app(test_config = None):
    app = Flask(__name__,
                instance_path=r'C:\Users\Николай\PycharmProjects\flask_tutorial\instance',
                instance_relative_config=True)

    app.config.from_mapping(
        DEBUG='True',
        SECRET_KEY='gln',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') # connect to sqlite
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config, if passed
        app.config.from_mapping(test_config)

    print(app.instance_path)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except:
        OSError

    # simple hello world
    @app.route('/')
    def hello_world():
        return 'Hello, Lord!'

    # register the database commands
    from . import db
    db.init_app(app)

    # register blueprint
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .blog import blog
    app.register_blueprint(blog)
    app.add_url_rule('/', endpoint='index')

    return app



create_app()