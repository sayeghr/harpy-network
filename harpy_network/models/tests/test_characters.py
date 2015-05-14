from harpy_network.models.characters import Character


class TestCharacterModel(object):

    def test_create_character(self):
        character = Character("Kashif Al-Tariq")
        assert isinstance(character, Character), "Unable to create a Character object."
        assert character.name == "Kashif Al-Tariq", "The name was not initialized properly."