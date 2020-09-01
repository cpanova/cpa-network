from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer


class LandingTestCase(APITestCase):
    url = '/api/offers/1/landings/'

    def setUp(self):
        super(LandingTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            id=1, is_staff=True, is_superuser=True, **credentials)
        self.client.login(**credentials)
        Offer.objects.create(id=1, title='a', description='a')

    def test_create(self):
        data = {
            'name': 'reg',
            'url': 'https://ya.ru',
            'preview_url': '...',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

        landing = response.json()
        self.assertEqual(landing['name'], 'reg')
