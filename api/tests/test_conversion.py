from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer, Currency, Goal, Payout


class ConversionTestCase(APITestCase):
    url = '/api/conversions/'

    def setUp(self):
        super(ConversionTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            id=1, is_staff=True, is_superuser=True, **credentials)
        self.client.login(**credentials)
        Offer.objects.create(id=1, title='a', description='a')
        Currency.objects.create(id=1, code="USD", name="Dollar")
        Goal.objects.create(id=6, name='Lead')

    def test_create(self):
        data = {
            "offer_id": 1,
            "pid": 1,
            "goal": '1',
            "goal_id": 6,
            "revenue": 32,
            "payout": 28,
            "currency": 'USD',
            "status": "hold",
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(201, response.status_code)

        conversion = response.json()
        self.assertEqual(conversion['offer_id'], 1)
        self.assertEqual(conversion['affiliate_id'], 1)
        self.assertEqual(conversion['goal_value'], '1')
        self.assertEqual(float(conversion['revenue']), 32)
        self.assertEqual(float(conversion['payout']), 28)
        self.assertEqual(conversion['currency']['code'], 'USD')
        self.assertEqual(conversion['status'], 'hold')
        self.assertEqual(conversion['goal']['name'], 'Lead')
