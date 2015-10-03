import pytest

from harpy_network.models.status import Status, InvalidStatusTraitError
from harpy_network.models.characters import Character


class TestStatusModel(object):

    def test_create_status(self):
        kashif = Character("Kashif Al-Tariq")
        status = Status(kashif, "Victorious", "Burlington, ON", "He was truly victorious.")
        assert isinstance(status, Status), "Unable to create the status object."
        assert status in kashif.status, "The status was not stored in the characters status list."

    def test_fail_with_invalid_status(self):
        """
        Test to make sure using an invalid status trait would cause an exception.
        """
        kashif = Character("Kashif Al-Tariq")
        with pytest.raises(InvalidStatusTraitError):
            status = Status(kashif, "Brutal", "Burlington, ON", "He was truly brutal.")