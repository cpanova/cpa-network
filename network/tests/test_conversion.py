import uuid
import pytz
import datetime
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer.models import Offer
from tracker.models import Conversion


class ConversionTestCase(APITestCase):
    list_url = '/network/conversions/'

    def setUp(self):
        super(ConversionTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(
            is_staff=True, **credentials)
        self.client.login(**credentials)
        self.offer = Offer.objects.create(
            title='blabla',
            description='blabla'
        )
        for x in range(3):
            Conversion.objects.create(
                click_id=uuid.uuid4(),
                click_date=datetime.datetime.now(pytz.UTC),
                revenue=0.0,
                payout=0.0,
                ip="1.1.1.1",
                affiliate_id=self.user.id,
                offer_id=self.offer.id
            )

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('offer_id', response.data[0])
        self.assertEqual(self.offer.id, response.data[0]['offer_id'])
        # self.assertIn('description', response.data[0])
        # self.assertIn('stop_at', response.data[0])
