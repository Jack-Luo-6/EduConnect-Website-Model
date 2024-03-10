from flask import Flask
import os
def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='education_connect',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')

    from . import personal_information
    app.register_blueprint(personal_information.bp)

    from . import reply
    app.register_blueprint(reply.bp)

    from . import about
    app.register_blueprint(about.bp)

    from . import search
    app.register_blueprint(search.bp)

    from . import open_ai
    app.register_blueprint(open_ai.bp)

    return app

