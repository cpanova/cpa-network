from django.test import TestCase
from countries_plus.models import Country
from ..tasks.conversion import conversion
from ..models import Click, Conversion
from django.contrib.auth import get_user_model
from offer.models import Offer, Payout, Currency


class TestConversionTask(TestCase):

    def setUp(self):
        super(TestConversionTask, self).setUp()
        self.user = (
            get_user_model().objects
            .create_user(username='aff', password='1234')
        )
        self.offer = Offer.objects.create(
            id=1, title='blabla', description='blabla'
        )

    def test_conversion_create(self):
        cl = Click.objects.create(
            ip='4.4.4.4',
            revenue=0,
            payout=0,
            offer=self.offer,
            affiliate=self.user
        )
        data = {
            'click_id': cl.id,
            'goal': 1,
            'sum': 0
        }
        conversion(data)
        self.assertTrue(
            Conversion.objects
            .filter(click_id=cl.id)
            .count()
        )

    def test_with_status(self):
        cl = Click.objects.create(
            ip='4.4.4.4',
            country='US',
            revenue=0,
            payout=0,
            offer=self.offer,
            affiliate=self.user
        )
        p = Payout.objects.create(
            revenue=0,
            payout=0,
            goal_value='1',
            offer=cl.offer,
            currency=Currency.objects.create(code='USD', name='USD'),
        )
        p.countries.add(
            Country.objects.create(
                iso='US', iso3='USA', iso_numeric=1, name='USA'
            )
        )
        data = {
            'click_id': cl.id,
            'goal': 1,
            'sum': 0,
            'status': 'approved'
        }
        conversion(data)
        cv = (
            Conversion.objects
            .filter(click_id=cl.id)
            .first())
        self.assertEquals(cv.status, 'approved')
