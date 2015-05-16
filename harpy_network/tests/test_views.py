from flask.ext.testing import TestCase
from flask.ext.login import current_user

from harpy_network import app, db
from harpy_network.models.users import User
from config import TestConfig

class TestViews(TestCase):

    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_splash_page(self):
        response = self.client.get('/')
        self.assert200(response, "Unable to load the splash page.")

    def test_login_and_logout(self):
        user = User("test@test.com", "password")
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post('/login',
                                        data={
                                            'email': 'test@test.com',
                                            'password': 'password'
                                        },
                                        follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the login url.")
            self.assertEqual(current_user, user, "The user is not the current user.")
            response = self.client.get('/logout',
                                       follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the logout url.")
            self.assertNotEqual(current_user, user, "The user is still logged in after attempting to log out.")

    def test_invalid_login(self):
        user = User("test@test.com", "password")
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post('/login',
                                        data={
                                            'email': 'test@test.com',
                                            'password': 'invalidpassword'
                                        },
                                        follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the login url.")
            self.assertNotEqual(current_user, user, "The user was logged in with an invalid password.")