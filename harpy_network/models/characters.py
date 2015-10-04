from harpy_network import db


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), unique=True)

    def __init__(self, name):
        self.name = name

    def merge_character(self, character):
        """
        Merges the provided character and it's associated boons to the instanced character object.
        """
        for boon_earned in character.boons_earned[:]:
            boon_earned.creditor = self
        for boon_owed in character.boons_owed[:]:
            boon_owed.debtor = self
        for status_trait in character.status[:]:
            status_trait.character = self
        db.session.delete(character)
