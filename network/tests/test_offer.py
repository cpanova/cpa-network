from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer, Advertiser


class OfferTestCase(APITestCase):
    list_url = '/network/offers/'
    retrieve_url = '/network/offers/1/'

    def setUp(self):
        super(OfferTestCase, self).setUp()
        credentials = {
            'username': 'staff',
            'password': '1234',
        }
        self.user = (
            get_user_model().objects
            .create_user(is_staff=True, **credentials)
        )
        self.client.login(**credentials)
        self.offers = [
            Offer.objects.create(
                id=offer_id,
                title='blabla',
                description='blabla',
                advertiser=(
                    Advertiser.objects
                    .create(company='x', email='x', comment='x')
                )
            ) for offer_id in range(3)
        ]

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('title', response.data[0])
        self.assertIn('description', response.data[0])

    def test_retrieve(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)
        self.assertIn('tracking_link', response.data)
        self.assertIn('preview_link', response.data)
        self.assertIn('countries', response.data)
        self.assertIn('status', response.data)
        self.assertIn('advertiser', response.data)
        self.assertIn('company', response.data['advertiser'])
        self.assertIn('categories', response.data)
        self.assertIn('traffic_sources', response.data)
        self.assertIn('payouts', response.data)
