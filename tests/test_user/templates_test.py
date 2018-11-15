from tests.base_test import BaseTestCase


class TestRouteToPages(BaseTestCase):
    render_templates = False

    def test_about_page(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('about.html')

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('register.html')

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('login.html')
