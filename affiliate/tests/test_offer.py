from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer


class OfferTestCase(APITestCase):
    list_url = '/affiliate/offers/'
    retrieve_url = '/affiliate/offers/1/'
    tracking_link_url = '/affiliate/offers/1/tracking-link/'

    def setUp(self):
        super(OfferTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(**credentials)
        self.client.login(**credentials)
        self.offers = [
            Offer.objects.create(
                id=x,
                title='blabla',
                description='blabla'
            ) for x in range(3)
        ]

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('title', response.data[0])
        self.assertIn('description', response.data[0])
        # self.assertIn('stop_at', response.data[0])

    def test_retrieve(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)
        self.assertIn('preview_link', response.data)
        self.assertIn('countries', response.data)
        self.assertIn('categories', response.data)
        self.assertIn('traffic_sources', response.data)
        self.assertIn('payouts', response.data)

    def test_tracking_link(self):
        response = self.client.get(self.tracking_link_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('url', response.data)
