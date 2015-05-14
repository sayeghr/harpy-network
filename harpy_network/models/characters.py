from harpy_network import db


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), unique=True)

    def __init__(self, name):
        self.name = name
