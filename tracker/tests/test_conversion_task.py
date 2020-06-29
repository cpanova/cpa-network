from django.test import TestCase
from ..tasks.conversion import conversion
from ..models import Click, Conversion
from django.contrib.auth import get_user_model
from offer.models import Offer


class TestConversionTask(TestCase):

    def setUp(self):
        super(TestConversionTask, self).setUp()
        user = (
            get_user_model().objects
            .create_user(username='aff', password='1234')
        )
        offer = Offer.objects.create(title='blabla', description='blabla')
        self.click = Click.objects.create(
            ip='4.4.4.4',
            revenue=0,
            payout=0,
            offer=offer,
            affiliate=user
        )

    def test_conversion_create(self):
        data = {
            'click_id': self.click.id,
            'goal': 1,
            'sum': 0
        }
        conversion(data)
        self.assertTrue(
            Conversion.objects
            .filter(click_id=self.click.id)
            .count()
        )
