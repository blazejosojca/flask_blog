from unittest import TestCase
from flask import url_for
from tests.base_test import BaseTest
from tests.base_test import (TEST_PASSWORD,
                             TEST_USER_EMAIL,
                             TEST_ADMIN_PASSWORD,
                             TEST_ADMIN_MAIL,
                             TEST_ADMIN_NAME,
                             TEST_USER_NAME)

from app.models import User, Post, load_user
from app import db


class TestModels(BaseTest):

    def test_user_model(self):
        self.assertEqual(User.query.count(), 2)

    def test_load_user(self):
        self.assertIsNotNone(load_user(1))

    def test_adding_new_user(self):
        user1 = User(username="test1", email="test1@mail.com")
        user1.set_password('password')
        db.session.add(user1)
        db.session.commit()
        self.assertEqual(User.query.count(), 3)

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

    def test_admin_dashboard_page(self):
        target_url = url_for('admin.admin_dashboard')
        response = self.app.get(target_url)
        redirect_url = url_for('auth.login')

        self.assertEqual(response.status_code, 302)


class TestLoginRoute(BaseTest):

    def test_login_with_correct_credentials(self):
        response = self.login(TEST_USER_EMAIL, TEST_PASSWORD)
        self.assertIn(b'You were logged in!', response.data)

    def test_login_page_with_empty_credentials(self):
        response = self.login('', '')
        self.assertIn(b'Log In!', response.data)

    def test_login_with_correct_admin_credentials(self):
        response = self.login(TEST_ADMIN_MAIL, TEST_ADMIN_PASSWORD)
        self.assertIn(b'You were logged in!', response.data)

    def test_login_with_incorrect_credentials(self):
        response = self.login('mail@mail.com', '123')
        self.assertIn(b'Credentials are incorrect!', response.data)

    def test_login_with_incorrect_email_format(self):
        response = self.login('test.mail.com', TEST_PASSWORD)
        self.assertIn(b'Invalid email address', response.data)

    def test_login_with_correct_email_incorrect_password(self):
        response = self.login(TEST_USER_EMAIL, '123')
        self.assertIn(b'Credentials are incorrect!', response.data)


class TestRegistrationRoute(BaseTest):

    def test_registration_with_data_of_existing_user(self):
        response = self.register(TEST_USER_NAME, TEST_USER_EMAIL, TEST_PASSWORD, TEST_PASSWORD)
        self.assertIn(b'This username already exists. Please use a different username!', response.data)

    def test_registration_with_valid_data(self):
        # response = self.register("new_test", 'new_test@mail.com', TEST_PASSWORD, TEST_PASSWORD)
        self.assertIsNotNone(User.query.filter_by(email="new_test@mail.com"))

    def test_registration_with_data_of_existing_admin(self):
        response = self.register(TEST_ADMIN_NAME, TEST_ADMIN_MAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_PASSWORD)
        self.assertIn(b'This username already exists. Please use a different username!', response.data)


class TestAdminRoute(BaseTest):

    def test_is_admin_current_user(self):
        logged_user = self.login(TEST_USER_EMAIL, TEST_PASSWORD)
        response = self.app.get(url_for('admin.admin_dashboard'), follow_redirects=True)
        self.assertEqual(response.status_code, 403)
