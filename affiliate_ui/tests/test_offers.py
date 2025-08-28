from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from offer.models import Offer, Category, Payout, Currency, Goal, ACTIVE_STATUS, PAUSED_STATUS
from affiliate_ui.views.general_views import generate_tracking_link


class OfferListViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser_offers'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.offers_url = reverse('affiliate_ui:offer_list')
        self.login_url = reverse('affiliate_ui:login')

        self.category1 = Category.objects.create(name='Finance')
        self.category2 = Category.objects.create(name='E-commerce')

        self.currency = Currency.objects.create(code='USD', name='US Dollar')
        self.goal = Goal.objects.create(name='Test Goal')

        self.offer1 = Offer.objects.create(title='Credit Card Offer', description='Financial offer', status=ACTIVE_STATUS)
        self.offer1.categories.add(self.category1)
        Payout.objects.create(offer=self.offer1, revenue=10, payout=5, currency=self.currency, goal=self.goal)

        self.offer2 = Offer.objects.create(title='Online Store Discount', description='Retail offer', status=ACTIVE_STATUS)
        self.offer2.categories.add(self.category2)
        Payout.objects.create(offer=self.offer2, revenue=20, payout=10, currency=self.currency, goal=self.goal)

        self.offer3 = Offer.objects.create(title='Inactive Offer', description='Should not be visible', status=PAUSED_STATUS)

    def test_offer_list_view_login_required(self):
        response = self.client.get(self.offers_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.offers_url}')

    def test_offer_list_view_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.offers_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/offers.html')

    def test_offer_list_displays_offers(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.offers_url)
        self.assertContains(response, 'Credit Card Offer')
        self.assertContains(response, 'Online Store Discount')
        self.assertNotContains(response, 'Inactive Offer')
        self.assertContains(response, '$5.00')
        self.assertContains(response, '$10.00')

    def test_offer_search(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.offers_url, {'search': 'Credit'})
        self.assertContains(response, 'Credit Card Offer')
        self.assertNotContains(response, 'Online Store Discount')

    def test_offer_filter_by_category(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.offers_url, {'category': self.category1.id})
        self.assertContains(response, 'Credit Card Offer')
        self.assertNotContains(response, 'Online Store Discount')


class OfferDetailViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser_offer_detail'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('affiliate_ui:login')

        self.currency = Currency.objects.create(code='USD', name='US Dollar')
        self.goal = Goal.objects.create(name='Test Goal')

        self.offer = Offer.objects.create(
            title='Detailed Offer',
            description_html='<p>Test Description</p>',
            status=ACTIVE_STATUS
        )
        Payout.objects.create(offer=self.offer, revenue=15, payout=7.5, currency=self.currency, goal=self.goal)
        self.offer_detail_url = reverse('affiliate_ui:offer_detail', args=[self.offer.id])

    def test_offer_detail_view_login_required(self):
        response = self.client.get(self.offer_detail_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.offer_detail_url}')

    def test_offer_detail_view_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.offer_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/offer_details.html')
        self.assertContains(response, 'Detailed Offer')
        self.assertContains(response, '<p>Test Description</p>')
        self.assertContains(response, '7.5') # Payout

    def test_tracking_link_generation(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.offer_detail_url)
        expected_link = f"{settings.TRACKER_URL}/click?offer_id={self.offer.id}&amp;pid={self.user.id}"
        self.assertContains(response, expected_link)

    def test_generate_tracking_link_function(self):
        offer_id = 1
        pid = 100
        expected_link = f"{settings.TRACKER_URL}/click?offer_id={offer_id}&pid={pid}"
        self.assertEqual(generate_tracking_link(offer_id, pid), expected_link)
