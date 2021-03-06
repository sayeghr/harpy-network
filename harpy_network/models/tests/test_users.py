from harpy_network.models.users import User


class TestUserModel(object):

    def test_create_user(self):
        user = User("test@test.com", "secret_password")
        assert isinstance(user, User), "Unable to create a user object."

    def test_set_user_password(self):
        user = User("test@test.com", "secret_password")
        user.set_password("new_secret_password")
        assert user.verify_password("new_secret_password"), "Unable to verify the new secret password."
        assert not user.verify_password("secret_password"), "New password was not stored with the user."