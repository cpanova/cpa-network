from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from datetime import date, timedelta

User = get_user_model()

class ReportViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_offer_report_view_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('offer_report'))
        self.assertRedirects(response, reverse('login') + '?next=/reports/offer/')

    @patch('affiliate_ui.views.report_views.offer_report')
    def test_offer_report_view_renders_with_data(self, mock_offer_report):
        mock_offer_report.return_value = [{'offer_name': 'Test Offer', 'revenue': 100}]

        response = self.client.get(reverse('offer_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/offer_report.html')
        self.assertIn('data', response.context)
        self.assertEqual(response.context['data'], [{'offer_name': 'Test Offer', 'revenue': 100}])

    @patch('affiliate_ui.views.report_views.offer_report')
    def test_offer_report_view_date_filtering(self, mock_offer_report):
        start_date = date.today() - timedelta(days=10)
        end_date = date.today() - timedelta(days=5)
        mock_offer_report.return_value = []

        response = self.client.get(reverse('offer_report'), {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        self.assertEqual(response.status_code, 200)
        mock_offer_report.assert_called_once()
        args, kwargs = mock_offer_report.call_args
        self.assertEqual(args[1].date(), start_date)
        self.assertEqual(args[2].date(), end_date)
        self.assertEqual(response.context['start_date'], start_date.isoformat())
        self.assertEqual(response.context['end_date'], end_date.isoformat())

    @patch('affiliate_ui.views.report_views.offer_report')
    def test_offer_report_view_default_dates(self, mock_offer_report):
        mock_offer_report.return_value = []

        response = self.client.get(reverse('offer_report'))
        self.assertEqual(response.status_code, 200)
        mock_offer_report.assert_called_once()
        args, kwargs = mock_offer_report.call_args
        self.assertEqual(args[1].date(), date.today() - timedelta(days=6))
        self.assertEqual(args[2].date(), date.today())
        self.assertEqual(response.context['start_date'], (date.today() - timedelta(days=6)).isoformat())
        self.assertEqual(response.context['end_date'], date.today().isoformat())

    @patch('affiliate_ui.views.report_views.offer_report')
    def test_offer_report_view_start_date_after_end_date(self, mock_offer_report):
        start_date = date.today()
        end_date = date.today() - timedelta(days=5)
        mock_offer_report.return_value = []

        response = self.client.get(reverse('offer_report'), {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        self.assertEqual(response.status_code, 200)
        mock_offer_report.assert_not_called()
