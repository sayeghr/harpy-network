from mock import MagicMock

from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon
from harpy_network.models.status import Status
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
        boon3 = Boon(character2, character3, "minor")
        boon4 = Boon(character2, character3, "minor")
        status = Status(character2, "Acknowledged", "Burlington, ON", "He was acknowledged.")
        assert boon not in character1.boons_earned, "The first character should not have boon 1 assigned."
        assert boon in character2.boons_earned, "The boon was not recorded as being earned by character 2."
        assert boon3 in character2.boons_owed, "The boon was not recorded as being owed by character 2."
        assert status in character2.status, "The status was not recorded to character 2."
        assert status not in character1.status, "The status should not have been recorded to character 1"
        self.original_session = db.session  # Store the original session object so that we can restore it after.
        db.session = MagicMock()
        character1.merge_character(character2)
        db.session.delete.assert_called_once_with(character2)
        db.session = self.original_session  # Restore the original session object.
        assert boon in character1.boons_earned, "The boon was not transferred successfully."
        assert boon2 in character1.boons_earned, "This boon should not have been removed."
        assert boon not in character2.boons_earned, "The boon was not transferred successfully."
        assert boon3 in character1.boons_owed, "The boon owed was not transferred successfully."
        assert boon4 in character1.boons_owed, "The second boon owed was not transferred successfully."
        assert boon3 not in character2.boons_owed, "The boon owed was not transferred successfully."
        assert status not in character2.status, "The status was not transferred properly."
        assert status in character1.status, "The status was not transferred properly to character 1."
