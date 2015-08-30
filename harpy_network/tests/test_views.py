from flask.ext.testing import TestCase
from flask.ext.login import current_user

from harpy_network import create_app, db
from harpy_network.models.users import User
from harpy_network.models.characters import Character
from harpy_network.models.boons import Boon
from harpy_network.views import load_user
from config import TestConfig

class TestViews(TestCase):

    #render_templates = False

    def create_app(self):
        app = create_app(TestConfig)
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

    def test_view_all_kindred(self):
        kashif = Character("Kashif Al-Tariq")
        db.session.add(kashif)
        db.session.commit()
        with self.client:
            response = self.client.get('/kindred',
                                       follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the view kindred endpoint.")
            self.assertEqual(self.get_context_variable('characters')[0].name, "Kashif Al-Tariq")

    def test_add_kindred(self):
        kashif = Character.query.filter_by(name="Kashif Al-Tariq").first()
        self.assertIsNone(kashif, "The character already exists.")
        with self.client:
            response = self.client.post('/kindred/add',
                                        data={
                                            'name': "Kashif Al-Tariq"
                                        },
                                        follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the add kindred endpoint.")
            kashif = Character.query.filter_by(name="Kashif Al-Tariq").first()
            self.assertIsNotNone(kashif, "The character was not created.")

    def test_fail_add_kindred(self):
        self.assertEqual(len(Character.query.all()), 0, "There already exists a character in the database.")
        with self.client:
            too_long_name = "x" * 300
            response = self.client.post('/kindred/add',
                                        data={
                                            'name': too_long_name
                                        },
                                        follow_redirects=True)
            self.assertEqual(len(Character.query.all()), 0,
                             "The add kindred method accepted a character with too many characters.")

    def test_edit_kindred(self):
        kashif = Character("Kashif Al-Tariq")
        db.session.add(kashif)
        db.session.commit()
        self.assertTrue(kashif.name == "Kashif Al-Tariq")
        self.assertTrue(kashif.id == 1)
        with self.client:
            response = self.client.post('/kindred/1/edit',
                                        data={
                                            'id': 1,
                                            'name': "Kashif"
                                        },
                                        follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the edit kindred endpoint.")
        kashif = Character.query.filter_by(id=1).first()
        self.assertTrue(kashif.name == "Kashif", "The character name was not edited.")

    def test_merge_kindred_view(self):
        character1 = Character("Kashif Al-Tariq")
        character2 = Character("Kashif")
        character3 = Character("Artanis")
        boon = Boon(character3, character2, "trivial")
        boon2 = Boon(character3, character1, "trivial")
        db.session.add(character1)
        db.session.add(character2)
        db.session.add(character3)
        db.session.add(boon)
        db.session.add(boon2)
        db.session.commit()
        assert boon not in character1.boons_earned, "The first character should not have boon 1 assigned."
        assert boon in character2.boons_earned, "The boon was not recorded as being earned by character 2."
        with self.client:
            response = self.client.post('/kindred/{CHARACTER_ID}/merge'.format(CHARACTER_ID=character1.id),
                                        data={
                                            'merging_kindred': character2.id,
                                        },
                                        follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the merge kindred endpoint.")
        assert boon in character1.boons_earned, "The boon was not transferred successfully."
        assert boon2 in character1.boons_earned, "This boon should not have been removed."
        assert boon not in character2.boons_earned, "The boon was not transferred successfully."

    def test_fail_edit_kindred(self):
        kashif = Character("Kashif Al-Tariq")
        artanis = Character("Artanis")
        db.session.add(kashif)
        db.session.add(artanis)
        db.session.commit()
        self.assertTrue(kashif.name == "Kashif Al-Tariq")
        self.assertTrue(kashif.id == 1)
        with self.client:
            response = self.client.post('/kindred/1/edit',
                                        data={
                                            'id': 1,
                                            'name': "Artanis"
                                        },
                                        follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the edit kindred endpoint.")
        kashif = Character.query.filter_by(id=1).first()
        self.assertTrue(kashif.name == "Kashif Al-Tariq", "The character name was not edited.")

    def test_load_user(self):
        user = User("test@test.com", "password")
        db.session.add(user)
        db.session.commit()
        loaded_user = load_user(str(user.id))
        self.assertEqual(user, loaded_user)

    def test_view_prestation(self):
        with self.client:
            response = self.client.get('/prestation',
                                       follow_redirects=True)
            self.assert200(response, "Did not get a 200 response from the view boons endpoint.")
            self.assertIsNotNone(self.get_context_variable('boons'), "Boons was not sent to the template.")