from django.test import TestCase
from unittest import mock
from django.urls import reverse


class TestPostbackHanlder(TestCase):

    def test_returns_400(self):
        url = reverse('tracker-postback')
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    @mock.patch('tracker.views.conversion')
    def test_returns_200(self, mock_conversion):
        url = reverse('tracker-postback')
        response = self.client.get(url, {'click_id': 1, 'goal': 1})
        self.assertEqual(200, response.status_code)
        self.assertTrue(mock_conversion.delay.called)
