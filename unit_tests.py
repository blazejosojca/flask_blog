import unittest
import os
from flask import url_for

from flask_testing import TestCase

from app import app, db
from config import basedir
from app.models import User, Post

TEST_USER_NAME = 'test_user'
TEST_USER_EMAIL = 'test@mail.com'
TEST_PASSWORD = 'password'


class BaseTest(TestCase):
    # Base methods for starting and closing/ cleaning testing   enviroment
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        user = User(username=TEST_USER_NAME, email=TEST_USER_EMAIL)
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
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists(os.path.join(basedir, 'test.db'))
        self.assertTrue(tester)
    #
    # Base test methods for further using
    def register(self, username, email, password, password_confirmation):
        return self.app.post(
            '/register',
            data=dict(
                username=username,
                email=email,
                password=password,
                password_confirmation=password_confirmation
            ), follow_redirects=True)

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


class TestMainApp(BaseTest):

    def test_server_is_up(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists(os.path.join(basedir, 'test.db'))
        self.assertTrue(tester)

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
        user=User.query.filter_by(username='test_user').first()

        post1=Post(title='test title', content='test content', author=user)
        db.session.add(post1)
        db.session.commit()

        self.assertEqual(Post.query.count(), 2)

    def test_adding_new_post(self):
        user=User.query.filter_by(username='test_user').first()
        post1=Post(title='test title', content='test content', author=user)
        db.session.add(post1)
        db.session.commit()

        self.assertEqual(Post.query.count(), 2)

class TestRoutes(BaseTest):

    # Tests of loading crucial pages
    def test_home_page_loads(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('home.html')

    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Login Page' in response.data)

    def test_about_page_loads(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('about.html')

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('register.html')

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('login.html')

    def test_logout_page(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class TestDisplayingTemplates(BaseTest):
    pass

class TestLoginRoute(BaseTest):

    def test_login_with_correct_credentials(self):
        response = self.login(TEST_USER_EMAIL, TEST_PASSWORD)
        self.assertIn(b'You were logged in!', response.data)

    def test_login_page_with_empty_credentials(self):
        response = self.login('','')
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
