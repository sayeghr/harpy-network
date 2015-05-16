from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import config

app = Flask(__name__)
app.config.from_object(config.Config)
app.secret_key = config.secret_key
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

import harpy_network.views
