from harpy_network import db


class Boon(db.Model):
    __tablename__ = "boon"
    id = db.Column(db.Integer, primary_key=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    creditor_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    weight = db.Column(db.String(20))
    comment = db.Column(db.Text)

    debtor = db.relationship("Character", foreign_keys=debtor_id, backref=db.backref("boons_owed"))
    creditor = db.relationship("Character", foreign_keys=creditor_id, backref=db.backref("boons_earned"))

    def __init__(self, debtor, creditor, weight):
        self.debtor = debtor
        self.creditor = creditor
        self.weight = weight
