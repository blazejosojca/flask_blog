from tests.base_test import BaseTestCase


class TestRoutes(BaseTestCase):

    # helper_functions
    def register(self, username, email, password, password_confirmation):
        return self.app.post(
            '/register',
            data=dict(
                username=username,
                email=email,
                password=password,
                password_confirmation=password_confirmation
            ),follow_redirects=True)

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True)

    def logout(self):
        return self.app.get('/logout',follow_redirects=True)
    # end of helper_functions

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
