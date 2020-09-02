from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class AdvertiserTestCase(APITestCase):
    url = '/api/advertisers/'

    def setUp(self):
        super(AdvertiserTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            id=1, is_staff=True, is_superuser=True, **credentials)
        self.client.login(**credentials)

    def test_create(self):
        data = {
            'company': 'ROX',
            'email': '...',
            'comment': '...',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

        offer = response.json()
        self.assertEqual(offer['company'], "ROX")
