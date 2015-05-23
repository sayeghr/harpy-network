from datetime import datetime

from harpy_network import db


class Boon(db.Model):
    __tablename__ = "boon"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.now)
    debtor_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    creditor_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    weight = db.Column(db.String(20))
    comment = db.Column(db.Text)
    paid = db.Column(db.Boolean, default=False)
    paid_at = db.Column(db.DateTime)

    debtor = db.relationship("Character", foreign_keys=debtor_id, backref=db.backref("boons_owed"))
    creditor = db.relationship("Character", foreign_keys=creditor_id, backref=db.backref("boons_earned"))

    @property
    def weight_string(self):
        if self.weight == "trivial":
            return "Trivial Boon"
        elif self.weight == "minor":
            return "Minor Boon"
        elif self.weight == "major":
            return "Major Boon"
        elif self.weight == "blood":
            return "Blood Boon"
        elif self.weight == "life":
            return "Life Boon"

    def __init__(self, debtor, creditor, weight):
        self.debtor = debtor
        self.creditor = creditor
        self.weight = weight
