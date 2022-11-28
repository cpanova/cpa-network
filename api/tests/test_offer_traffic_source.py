from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer, TrafficSource


class OfferTrafficSourceTestCase(APITestCase):
    url = '/api/traffic-sources/'

    def setUp(self):
        super(OfferTrafficSourceTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            id=1, is_staff=True, is_superuser=True, **credentials)
        self.client.login(**credentials)
        Offer.objects.create(id=1, title='a', description='a')
        TrafficSource.objects.create(id=1, name='a')

    def test_create(self):
        data = {
            'offer_id': 1,
            'traffic_source_id': 1,
            'allowed': False,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

        offer_traffic_source = response.json()
        self.assertEqual(offer_traffic_source['traffic_source']['id'], 1)
        self.assertEqual(offer_traffic_source['allowed'], False)
