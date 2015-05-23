from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_object):

    app = Flask(__name__)
    app.config.from_object(config_object)
    app.secret_key = config.secret_key
    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    # Initialize Blueprints
    from harpy_network.views import views
    app.register_blueprint(views)

    return app

app = create_app(config.Config)

