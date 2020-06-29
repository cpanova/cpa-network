import uuid
import pytz
import datetime
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer
from tracker.models import Click, Conversion


class StatsTestCase(APITestCase):
    offers_stats_url = '/affiliate/stats/offers/'
    daily_stats_url = '/affiliate/stats/daily/'

    def setUp(self):
        super(StatsTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(**credentials)
        self.client.login(**credentials)
        self.offer = Offer.objects.create(
            title='blabla',
            description='blabla'
        )
        sample_values = {
            'affiliate_id': self.user.id,
            'offer_id': self.offer.id,
            'ip': '1.1.1.1',
            'revenue': 0.0,
            'payout': 0.0
        }
        for _ in range(100):
            Click.objects.create(**sample_values)
        for _ in range(3):
            Conversion.objects.create(
                click_id=uuid.uuid4(),
                click_date=datetime.datetime.now(pytz.UTC),
                **sample_values
            )

    def test_offers_stats(self):
        response = self.client.get(self.offers_stats_url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(bool(len(response.data)))
        self.assertIn('offer_id', response.data[0])
        self.assertIn('offer_title', response.data[0])
        self.assertIn('clicks', response.data[0])
        self.assertTrue(response.data[0]['clicks'] == 100)
        self.assertIn('total_qty', response.data[0])
        self.assertIn('approved_qty', response.data[0])
        self.assertIn('hold_qty', response.data[0])
        self.assertIn('rejected_qty', response.data[0])
        self.assertIn('cr', response.data[0])
        self.assertIn('approved_payout', response.data[0])
        self.assertIn('hold_payout', response.data[0])
        self.assertIn('rejected_payout', response.data[0])
        self.assertIn('total_payout', response.data[0])

    def test_daily_stats(self):
        response = self.client.get(self.daily_stats_url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(bool(len(response.data)))
        self.assertIn('date', response.data[0])
        self.assertIn('clicks', response.data[0])
        self.assertTrue(response.data[0]['clicks'] == 100)
        self.assertIn('total_qty', response.data[0])
        self.assertIn('approved_qty', response.data[0])
        self.assertIn('hold_qty', response.data[0])
        self.assertIn('rejected_qty', response.data[0])
        self.assertIn('cr', response.data[0])
        self.assertIn('approved_payout', response.data[0])
        self.assertIn('hold_payout', response.data[0])
        self.assertIn('rejected_payout', response.data[0])
        self.assertIn('total_payout', response.data[0])
