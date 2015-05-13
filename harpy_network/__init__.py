from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config.Config)
app.secret_key = config.secret_key
db = SQLAlchemy(app)

import harpy_network.views