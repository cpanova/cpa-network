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

    def test_daily_report_view_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('affiliate_ui:daily_report'))
        self.assertRedirects(response, reverse('affiliate_ui:login') + '?next=/reports/daily/')

    @patch('affiliate_ui.views.report_views.daily_report')
    @patch('offer.models.Offer.objects')
    def test_daily_report_view_renders_with_data(self, mock_offer_objects, mock_daily_report):
        mock_daily_report.return_value = [{'date': '2025-08-01', 'clicks': 10, 'conversions': 2}]
        mock_offer_objects.filter.return_value.distinct.return_value = []

        response = self.client.get(reverse('affiliate_ui:daily_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/daily_report.html')
        self.assertIn('data', response.context)
        self.assertIn('offers', response.context)
        self.assertEqual(response.context['data'], [{'date': '2025-08-01', 'clicks': 10, 'conversions': 2}])

    @patch('affiliate_ui.views.report_views.daily_report')
    @patch('offer.models.Offer.objects')
    def test_daily_report_view_date_filtering(self, mock_offer_objects, mock_daily_report):
        start_date = date.today() - timedelta(days=10)
        end_date = date.today() - timedelta(days=5)
        mock_daily_report.return_value = []
        mock_daily_report.reset_mock()
        mock_offer_objects.filter.return_value.distinct.return_value = []

        response = self.client.get(reverse('affiliate_ui:daily_report'), {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        self.assertEqual(response.status_code, 200)
        mock_daily_report.assert_called_once()
        args, kwargs = mock_daily_report.call_args
        self.assertEqual(args[1].date(), start_date)
        self.assertEqual(args[2].date(), end_date)
        self.assertEqual(response.context['start_date'], start_date.isoformat())
        self.assertEqual(response.context['end_date'], end_date.isoformat())

    @patch('affiliate_ui.views.report_views.daily_report')
    @patch('offer.models.Offer.objects')
    def test_daily_report_view_offer_filtering(self, mock_offer_objects, mock_daily_report):
        mock_daily_report.return_value = []
        mock_offer_objects.filter.return_value.distinct.return_value = []

        response = self.client.get(reverse('affiliate_ui:daily_report'), {'offer_id': '123'})
        self.assertEqual(response.status_code, 200)
        mock_daily_report.assert_called_once()
        args, kwargs = mock_daily_report.call_args
        self.assertEqual(args[3], 123)
        self.assertEqual(response.context['selected_offer_id'], 123)

    @patch('affiliate_ui.views.report_views.daily_report')
    @patch('offer.models.Offer.objects')
    def test_daily_report_view_default_dates_and_offer_id(self, mock_offer_objects, mock_daily_report):
        mock_daily_report.return_value = []
        mock_offer_objects.filter.return_value.distinct.return_value = []

        response = self.client.get(reverse('affiliate_ui:daily_report'))
        self.assertEqual(response.status_code, 200)
        mock_daily_report.assert_called_once()
        args, kwargs = mock_daily_report.call_args
        self.assertEqual(args[1].date(), date.today() - timedelta(days=6))
        self.assertEqual(args[2].date(), date.today())
        self.assertEqual(args[3], 0)
        self.assertIsNone(response.context['selected_offer_id'])
        self.assertEqual(response.context['start_date'], (date.today() - timedelta(days=6)).isoformat())
        self.assertEqual(response.context['end_date'], date.today().isoformat())

    @patch('affiliate_ui.views.report_views.daily_report')
    @patch('offer.models.Offer.objects')
    def test_daily_report_view_start_date_after_end_date(self, mock_offer_objects, mock_daily_report):
        start_date = date.today()
        end_date = date.today() - timedelta(days=5)
        mock_daily_report.return_value = []
        mock_offer_objects.filter.return_value.distinct.return_value = []

        response = self.client.get(reverse('affiliate_ui:daily_report'), {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        self.assertEqual(response.status_code, 200)
        mock_daily_report.assert_not_called()
