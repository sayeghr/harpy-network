from flask.ext.testing import TestCase

from harpy_network import app, db

class TestViews(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_splash_page(self):
        response = self.client.get('/')
        self.assert200(response, "Unable to load the splash page.")