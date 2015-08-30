from mock import MagicMock

from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon
from harpy_network import db


class TestCharacterModel(object):

    def test_create_character(self):
        character = Character("Kashif Al-Tariq")
        assert isinstance(character, Character), "Unable to create a Character object."
        assert character.name == "Kashif Al-Tariq", "The name was not initialized properly."

    def test_merge_character(self):
        character1 = Character("Kashif Al-Tariq")
        character2 = Character("Kashif")
        character3 = Character("Artanis")
        boon = Boon(character3, character2, "trivial")
        boon2 = Boon(character3, character1, "trivial")
        assert boon not in character1.boons_earned, "The first character should not have boon 1 assigned."
        assert boon in character2.boons_earned, "The boon was not recorded as being earned by character 2."
        db.session = MagicMock()
        character1.merge_character(character2)
        db.session.delete.assert_called_once_with(character2)
        assert boon in character1.boons_earned, "The boon was not transferred successfully."
        assert boon2 in character1.boons_earned, "This boon should not have been removed."
        assert boon not in character2.boons_earned, "The boon was not transferred successfully."
