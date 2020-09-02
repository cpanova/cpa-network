from rest_framework.test import APITestCase
from countries_plus.models import Country
from django.contrib.auth import get_user_model


class OfferTestCase(APITestCase):
    url = '/api/offers/'

    def setUp(self):
        super(OfferTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            id=1, is_staff=True, is_superuser=True, **credentials)
        self.client.login(**credentials)
        Country.objects.create(
            iso='RU', iso3='RUS', iso_numeric=1, name='Russia'
        )

    def test_create(self):
        data = {
            "title": "test offer",
            'countries': ['RU']
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

        offer = response.json()
        self.assertEqual(offer['title'], "test offer")
