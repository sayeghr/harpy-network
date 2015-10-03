from collections import namedtuple
from datetime import datetime

from harpy_network import db


StatusTrait = namedtuple("StatusTrait", ["name", "type", "sect"])

status_traits = (
    StatusTrait("Acclaimed", "fleeting", "camarilla"),
    StatusTrait("Acknowledged", "accepted", "camarilla"),
    StatusTrait("Architect", "innate", "camarilla"),
    StatusTrait("Ascendant", "abiding", "camarilla"),
    StatusTrait("Authority", "abiding", "general"),
    StatusTrait("Commander", "abiding", "general"),
    StatusTrait("Confirmed", "abiding", "camarilla"),
    StatusTrait("Courteous", "fleeting", "general"),
    StatusTrait("Courageous", "fleeting", "general"),
    StatusTrait("Defender", "fleeting", "general"),
    StatusTrait("Disgraced", "negative", "general"),
    StatusTrait("Enforcer", "abiding", "general"),
    StatusTrait("Established", "abiding", "general"),
    StatusTrait("Favored", "fleeting", "general"),
    StatusTrait("Forsaken", "negative", "general"),
    StatusTrait("Gallant", "fleeting", "camarilla"),
    StatusTrait("Guardian", "abiding", "camarilla"),
    StatusTrait("Honorable", "fleeting", "general"),
    StatusTrait("Loyal", "fleeting", "general"),
    StatusTrait("Noble", "abiding", "camarilla"),
    StatusTrait("Praised", "fleeting", "general"),
    StatusTrait("Primus Inter Pares", "innate", "camarilla"),
    StatusTrait("Privileged", "abiding", "camarilla"),
    StatusTrait("Prominent", "abiding", "general"),
    StatusTrait("Sanctioned", "fleeting", "camarilla"),
    StatusTrait("Sovereign", "abiding", "camarilla"),
    StatusTrait("Triumphant", "fleeting", "general"),
    StatusTrait("Victorious", "fleeting", "general"),
    StatusTrait("Vulgar", "negative", "camarilla"),
    StatusTrait("Warned", "negative", "general")
)


class InvalidStatusTraitError(Exception):
    pass


class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.now)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    name = db.Column(db.String(20))
    sect = db.Column(db.String(20))
    type = db.Column(db.String(20))
    location_earned = db.Column(db.String(254))
    story = db.Column(db.Text)
    # relationships
    character = db.relationship("Character", foreign_keys=character_id, backref=db.backref("status"))

    def update_status_name(self, name):
        for status_trait in status_traits:
            if name.lower() == status_trait.name.lower():
                self.name = status_trait.name
                self.type = status_trait.type
                self.sect = status_trait.sect
                break
        else:
            # Invalid status trait name
            raise InvalidStatusTraitError

    def __init__(self, character, name, location_earned, story):
        self.character = character
        for status_trait in status_traits:
            if name.lower() == status_trait.name.lower():
                self.name = status_trait.name
                self.type = status_trait.type
                self.sect = status_trait.sect
                break
        else:
            # Invalid status trait name
            raise InvalidStatusTraitError
        self.location_earned = location_earned
        self.story = story
