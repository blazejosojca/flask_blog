import unittest
import os

from flask_testing import TestCase
from app import app, db
from config import basedir

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        self.app = app.test_client()

        db.create_all()


    def test_server_is_up(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists(os.path.join(basedir, 'test.db'))
        self.assertTrue(tester)

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

    def test_valid_user_login(self):
        response = self.login('test@mail.com', 'password')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'', str(response.data))

    def test_valid_user_registration(self):
            response = self.register('test', 'test@mail.com', 'password', 'password')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login Page', response.data)

    def test_home_page(self):
            response = self.app.get('/home', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('home.html')

    def test_about_page(self):
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


    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
