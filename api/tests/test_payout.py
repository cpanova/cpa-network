from rest_framework.test import APITestCase
from countries_plus.models import Country
from django.contrib.auth import get_user_model
from offer.models import Offer, Currency, Goal


class PayoutTestCase(APITestCase):
    url = '/api/offers/1/payouts/'

    def setUp(self):
        super(PayoutTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            id=1, is_staff=True, is_superuser=True, **credentials)
        self.client.login(**credentials)
        Offer.objects.create(id=1, title='a', description='a')
        Currency.objects.create(id=1, code='USD', name='US Dollar')
        Goal.objects.create(id=1, name='Reg')
        Country.objects.create(iso='RU', iso3='RUS', iso_numeric=1, name='Russia')

    def test_create(self):
        data = {
            'revenue': '1.0',
            'payout': '0.8',
            'currency': 1,
            'goal': 1,
            'goal_value': '2',
            'countries': ['RU']
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

        payout = response.json()
        self.assertEqual(payout['goal_value'], '2')
        # self.assertEqual(payout['offer_id'], '1')
