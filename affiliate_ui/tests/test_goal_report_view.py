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

    def test_goal_report_view_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('goal_report'))
        self.assertRedirects(response, reverse('login') + '?next=/reports/goal/')

    @patch('affiliate_ui.views.report_views.goal_report')
    def test_goal_report_view_renders_with_data(self, mock_goal_report):
        mock_goal_report.return_value = [{'goal_name': 'Test Goal', 'count': 5}]

        response = self.client.get(reverse('goal_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'affiliate_ui/goal_report.html')
        self.assertIn('data', response.context)
        self.assertEqual(response.context['data'], [{'goal_name': 'Test Goal', 'count': 5}])

    @patch('affiliate_ui.views.report_views.goal_report')
    def test_goal_report_view_date_filtering(self, mock_goal_report):
        start_date = date.today() - timedelta(days=10)
        end_date = date.today() - timedelta(days=5)
        mock_goal_report.return_value = []

        response = self.client.get(reverse('goal_report'), {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        self.assertEqual(response.status_code, 200)
        mock_goal_report.assert_called_once()
        args, kwargs = mock_goal_report.call_args
        self.assertEqual(args[1].date(), start_date)
        self.assertEqual(args[2].date(), end_date)
        self.assertEqual(response.context['start_date'], start_date.isoformat())
        self.assertEqual(response.context['end_date'], end_date.isoformat())

    @patch('affiliate_ui.views.report_views.goal_report')
    def test_goal_report_view_default_dates(self, mock_goal_report):
        mock_goal_report.return_value = []
        mock_goal_report.reset_mock()

        response = self.client.get(reverse('goal_report'))
        self.assertEqual(response.status_code, 200)
        mock_goal_report.assert_called_once()
        args, kwargs = mock_goal_report.call_args
        self.assertEqual(args[1].date(), date.today() - timedelta(days=6))
        self.assertEqual(args[2].date(), date.today())
        self.assertEqual(response.context['start_date'], (date.today() - timedelta(days=6)).isoformat())
        self.assertEqual(response.context['end_date'], date.today().isoformat())

    @patch('affiliate_ui.views.report_views.goal_report')
    def test_goal_report_view_start_date_after_end_date(self, mock_goal_report):
        start_date = date.today()
        end_date = date.today() - timedelta(days=5)
        mock_goal_report.return_value = []

        response = self.client.get(reverse('goal_report'), {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
        self.assertEqual(response.status_code, 200)
        mock_goal_report.assert_called_once()
        args, kwargs = mock_goal_report.call_args
        self.assertEqual(args[1].date(), start_date)
        self.assertEqual(args[2].date(), end_date)
