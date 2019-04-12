# unit_tests.py

import unittest
import os
from flask import url_for, current_app

from flask_testing import TestCase

from app import create_app, db
from config import BASEDIR, Config
from app.models import User, Post


# setting testing variables for test user
TEST_USER_NAME = 'test_user'
TEST_USER_EMAIL = 'test@mail.com'
TEST_PASSWORD = 'password'
TEST_ADMIN_NAME = 'test_admin'
TEST_ADMIN_MAIL = 'admin@mail.com'
TEST_ADMIN_PASSWORD = 'admin123'


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'test.db')


class BaseTest(TestCase):

    def create_app(self):
        app = create_app(TestConfig)

        return app

    def setUp(self):
        self.app = current_app.test_client()

        db.create_all()

        user = User(username=TEST_USER_NAME,
                    email=TEST_USER_EMAIL)
        user.set_password('password')
        post = Post(title='test title', content='test content', author=user)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        admin = User(username=TEST_ADMIN_NAME,
                     email=TEST_ADMIN_MAIL)
        admin.set_password('admin123')
        admin.is_admin = True

        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests for ensure that flask is set up
    def test_server_is_up(self):
        tester = current_app.test_client(self)
        response = tester.get(url_for('main.home'), content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists(os.path.join(BASEDIR, 'test.db'))
        self.assertTrue(tester)

    # Base test methods for further using
    def register(self, username, email, password, password_confirmation):
        return self.app.post(
            '/auth/register',
            data=dict(
                username=username,
                email=email,
                password=password,
                password_confirmation=password_confirmation
            ), follow_redirects=True)

    def login(self, email, password):
        return self.app.post(
            '/auth/login',
            data=dict(email=email, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
