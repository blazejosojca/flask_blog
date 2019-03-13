import unittest
import os
from flask import url_for, current_app

from flask_testing import TestCase

from app import create_app, db
from config import basedir, Config
from app.models import User, Post

TEST_USER_NAME = 'test_user'
TEST_USER_EMAIL = 'test@mail.com'
TEST_PASSWORD = 'password'


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests for ensure that flask is set up
    def test_server_is_up(self):
        tester = current_app.test_client(self)
        response = tester.get(url_for('main.home'), content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists(os.path.join(basedir, 'test.db'))
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


class TestModels(BaseTest):

    def test_user_model(self):
        self.assertEqual(User.query.count(), 1)

    def test_adding_new_user(self):
        user1 = User(username="test1", email="test1@mail.com")
        user1.set_password('password')
        db.session.add(user1)
        db.session.commit()
        self.assertEqual(User.query.count(), 2)

    def test_post_model(self):
        user = User.query.filter_by(username='test_user').first()
        post1 = Post(title='test title',
                     content='test content',
                     author=user)
        db.session.add(post1)
        db.session.commit()

        self.assertEqual(Post.query.count(), 2)

    def test_adding_new_post(self):
        user = User.query.filter_by(username='test_user').first()
        post1 = Post(title='test title',
                     content='test content',
                     author=user)
        db.session.add(post1)
        db.session.commit()

        self.assertEqual(Post.query.count(), 2)


class TestRoutes(BaseTest):

    # Tests of loading crucial pages
    def test_home_page_loads(self):
        response = self.app.get(url_for('main.home'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main/home.html')

    def test_login_page_loads(self):
        response = self.app.get(url_for('auth.login'), content_type='html/text')
        self.assertTrue(b'Log In!' in response.data)

    def test_about_page_loads(self):
        response = self.app.get(url_for('main.about'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main/about.html')

    def test_register_page(self):
        response = self.app.get(url_for('auth.register'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('auth/register.html')

    def test_login_page(self):
        response = self.app.get(url_for('auth.login'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('auth/login.html')

    def test_logout_page(self):
        response = self.app.get(url_for('auth.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class TestDisplayingTemplates(BaseTest):
    pass


class TestLoginRoute(BaseTest):

    def test_login_with_correct_credentials(self):
        response = self.login(TEST_USER_EMAIL, TEST_PASSWORD)
        self.assertIn(b'You were logged in!', response.data)

    def test_login_page_with_empty_credentials(self):
        response = self.login('', '')
        self.assertIn(b'Log In!', response.data)


class TestRegistrationRoute(BaseTest):

    def test_registration_with_data_of_existing_user(self):
        response = self.register(TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD, TEST_PASSWORD)
        self.assertIn(b'This username already exists. Please use a different username!', response.data)

    def test_registration_with_valid_data(self):
        response = self.register("new_test", 'new_test@mail.com', TEST_PASSWORD, TEST_PASSWORD)
        self.assertIn(b'Login Page', response.data)


if __name__ == '__main__':
    unittest.main()
