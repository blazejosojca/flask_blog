import unittest
from flask_testing import TestCase

from app import app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == 'main':
    unittest.main()