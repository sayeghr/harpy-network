from passlib.hash import bcrypt
from flask.ext.login import UserMixin

from harpy_network import db

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(60))
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.set_password(password)
        self.admin = admin

    def set_password(self, password):
        self.password = bcrypt.encrypt(password)
        return self.password

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
