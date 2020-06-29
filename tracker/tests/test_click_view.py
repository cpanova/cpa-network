from django.test import TestCase
from unittest import mock
from django.urls import reverse


class TestClickHanlder(TestCase):

    @mock.patch('tracker.dao.TrackerCache')
    def test_it_returns_400(self, mock_tracker_cache):
        url = reverse('tracker-click')
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    @mock.patch('tracker.dao.TrackerCache.get_offer', return_value=None)
    def test_it_returns_404(self, mock_tracker_cache):
        url = reverse('tracker-click')
        response = self.client.get(url, {'pid': 1, 'offer_id': 1})
        self.assertEqual(404, response.status_code)

    @mock.patch('tracker.views.click_task')
    @mock.patch(
        'tracker.dao.TrackerCache.get_offer',
        return_value={'tracking_link': 'http://example.com'}
    )
    def test_it_returns_302(self, mock_tracker_cache, mock_click_task):
        url = reverse('tracker-click')
        response = self.client.get(
            url,
            {'pid': 1, 'offer_id': 1},
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEqual(302, response.status_code)
        self.assertTrue(mock_click_task.delay.called)
