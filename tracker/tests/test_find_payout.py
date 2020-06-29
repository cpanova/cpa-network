# from django.test import TestCase
# from unittest import mock
# from django.urls import reverse
# from offer.models import Offer, Payout, Advertiser, Currency
# from ..dao import find_payout


# class TestFindPayout(TestCase):

#     def setUp(self):
#         super(TestFindPayout, self).setUp()
#         Offer.objects.create(
#             id=1,
#             title='blabla',
#             description='blabla',
#             advertiser=Advertiser.objects.create(
#                 company='x',
#                 email='x',
#                 comment='x'
#             )
#         )
#         payout = Payout.objects.create(
#             offer_id=1,
#             revenue=0,
#             payout=0,
#             goal_value='2',
#             currency=Currency.objects.create(code='USD', name='Dollar')
#         )
#         payout.countries.add('RU')

#     def test_payout_found(self):
#         self.assertTrue(bool(find_payout(1, 'RU', '2')))
