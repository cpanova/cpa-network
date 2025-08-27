from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/login.html')

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, follow=True)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_fail(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_already_logged_in_redirect(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url, follow=True)
        self.assertRedirects(response, self.dashboard_url)
