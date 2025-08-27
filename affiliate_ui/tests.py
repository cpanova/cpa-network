from decimal import Decimal
from django.test import TestCase
from django.apps import apps
from django.contrib.auth.models import User
from django.urls import reverse

from offer.models import Offer, Category, Payout, Currency, Goal, ACTIVE_STATUS, PAUSED_STATUS
from tracker.models import Click, Conversion, APPROVED_STATUS, PENDING_STATUS


class AffiliateUiConfigTest(TestCase):
    def test_app_config(self):
        self.assertEqual(apps.get_app_config('affiliate_ui').name, 'affiliate_ui')


class LoginTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/login.html')

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, follow=True)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_fail(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_already_logged_in_redirect(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url, follow=True)
        self.assertRedirects(response, self.dashboard_url)


class DashboardTest(TestCase):
    def setUp(self):
        self.username = 'testuser_dashboard'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('login')

        # Create test data
        Click.objects.create(affiliate=self.user, ip='127.0.0.1', revenue=Decimal('0.5'), payout=Decimal('0.2'))
        Click.objects.create(affiliate=self.user, ip='127.0.0.1', revenue=Decimal('0.6'), payout=Decimal('0.3'))

        Conversion.objects.create(affiliate=self.user, status=APPROVED_STATUS, payout=Decimal('10.50'))
        Conversion.objects.create(affiliate=self.user, status=APPROVED_STATUS, payout=Decimal('5.25'))
        Conversion.objects.create(affiliate=self.user, status=PENDING_STATUS, payout=Decimal('20.00'))

    def test_dashboard_unauthenticated_redirect(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f'{self.login_url}?next={self.dashboard_url}')

    def test_dashboard_authenticated_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/dashboard.html')

        # Check context data
        self.assertEqual(response.context['clicks_count'], 2)
        self.assertEqual(response.context['conversions_count'], 3)
        self.assertEqual(response.context['total_earnings'], '15.75')

        # Check rendered HTML
        self.assertContains(response, '<p class="card-text fs-2">2</p>', html=True)
        self.assertContains(response, '<p class="card-text fs-2">3</p>', html=True)
        self.assertContains(response, '<p class="card-text fs-2">$15.75</p>', html=True)


class OfferListViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser_offers'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.offers_url = reverse('offer_list')
        self.login_url = reverse('login')

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
