from django.test import TestCase
from django.apps import apps


class AffiliateUiConfigTest(TestCase):
    def test_app_config(self):
        self.assertEqual(apps.get_app_config('affiliate_ui').name, 'affiliate_ui')
