"""Unit test for the user application"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class LoginTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'x8kFVJMvcqVaqxT'
        }
        User.objects.create_user(**self.credentials)

    def test_login_page_status_code(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_login_url_by_name(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_login_uses_correct_template(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_valid_user_login(self):
        response = self.client.post(reverse('user:login'), self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_valid_user_login_redirect_home(self):
        response = self.client.post(reverse('user:login'), self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertRedirects(response, '/')

    def test_valid_user_uses_correct_template_after_login(self):
        response = self.client.post(reverse("user:login"), self.credentials, follow=True)
        self.assertTemplateUsed(response, 'home.html')

    def test_invalid_user_login(self):
        response = self.client.post(reverse('user:login'),
            {'username': "Ratatouille", 'password': 'FmrOaGe!'}, follow=True)
        self.assertFalse(response.context["user"].is_authenticated)


class LogoutTests(TestCase):
    def test_logout_page_status_code(self):
        response = self.client.get('/user/logout/')
        self.assertEqual(response.status_code, 302)

    def test_view_logout_url_by_name(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)

    def test_view_logout_uses_correct_template(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    

class RegisterTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'AugusteGusteau',
            'email': 'auguste.gusteau@bocuse.com',
            'password1': 'EcSofFRie!',
            'password2': 'EcSofFRie!'
        }
        
    def test_register_page_status_code(self):
        response = self.client.get('/user/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_register_url_by_name(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_view_register_uses_correct_template(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    def test_valid_user_exists_after_registration(self):
        response = self.client.post(
            reverse('user:register'),
            {
                "username": self.credentials["username"],
                "email": self.credentials["email"],
                "password1": self.credentials["password1"],
                "password2": self.credentials["password2"],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='AugusteGusteau').exists())

    def test_valid_register_uses_correct_template(self):
        response = self.client.post(reverse('user:register'), self.credentials, follow=True)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_invalid_register_uses_correct_template(self):
        response = self.client.post(
            reverse('user:register'),
            {
                "username": self.credentials["username"],
                "email": self.credentials["email"],
                "password1": self.credentials["password1"],
                "password2": 'blabla',
            },
            follow=True,
        )
        self.assertTemplateUsed(response, 'user/register.html')


class AccountTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('AugusteGusteau', 'auguste.gusteau@bocuse.com', 'EcSofFRie!')
        self.client.login(username='AugusteGusteau', password='EcSofFRie!')
        
    def test_account_page_status_code(self):
        response = self.client.get('/user/account/')
        self.assertEqual(response.status_code, 200)

    def test_view_account_url_by_name(self):
        response = self.client.get(reverse('user:account'))
        self.assertEqual(response.status_code, 200)

    def test_view_account_uses_correct_template(self):
        response = self.client.get(reverse('user:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/account.html')
