import uuid
from django.test import TestCase
from ..tasks.click import click
from ..models import Click
from django.contrib.auth import get_user_model
from offer.models import Offer
from user_profile.models import Profile


class TestClickTask(TestCase):

    def setUp(self):
        super(TestClickTask, self).setUp()
        self.user = (
            get_user_model().objects
            .create_user(username='aff', password='1234')
        )
        manager = (
            get_user_model().objects
            .create_user(username='manager', password='1234')
        )
        Profile.objects.create(id=100, user=self.user, manager=manager)
        self.offer = Offer.objects.create(title='blabla', description='blabla')

    def test_click_create(self):
        click_id = uuid.uuid4()
        data = {
            'click_id': click_id,
            'offer_id': self.offer.id,
            'pid': self.user.id,
            'ip': '4.4.4.4',
            'ua': 'Mozilla /5.0',
            'sub1': '',
            'sub2': '',
            'sub3': '',
            'sub4': '',
            'sub5': ''
        }
        click(data)
        cl = Click.objects.get(pk=click_id)
        self.assertTrue(Click.objects.count())
        self.assertEquals(cl.country, 'US')
        self.assertEquals(cl.affiliate_manager_id, 100)
