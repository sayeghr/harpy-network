from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon


class TestCharacterModel(object):

    def test_create_boon(self):
        kashif = Character("Kashif Al-Tariq")
        artanis = Character("Artanis LeBlanc")
        trivial_boon = Boon(kashif, artanis, "trivial")
        assert trivial_boon.debtor == kashif, "Kashif was not set as the debtor of the Trivial boon."
        assert trivial_boon.creditor == artanis, "Artanis was not set as the creditor of the trivial boon."
        assert trivial_boon.weight == "trivial", "The boon was not registered as a trivial boon."