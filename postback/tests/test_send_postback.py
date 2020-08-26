from unittest.mock import patch
from django.test import TestCase
from ..tasks.send_postback import send_postback
from ..models import Postback


@patch('postback.tasks.send_postback.persist_log', autospec=True)
@patch('postback.tasks.send_postback.requests', autospec=True)
@patch('postback.tasks.send_postback.find_postbacks', autospec=True)
class TestSendPostback(TestCase):

    def setUp(self):
        super(TestSendPostback, self).setUp()

    def test_doesnt_send_postback(self, mocked_find_postbacks, mocked_requests, mocked_persist_log):
        postback = Postback()
        mocked_find_postbacks.return_value = []
        conversion = {
            'offer_id': 1,
            'affiliate_id': 2,
        }
        send_postback(conversion)
        assert not mocked_requests.get.called, 'requests should not be called'
        assert not mocked_persist_log.called, 'persist log should not be called'

    def test_sends_postback(self, mocked_find_postbacks, mocked_requests, mocked_persist_log):
        postback = Postback(url="http://example.com/path?sub1={sub1}&sum={sum}")
        mocked_find_postbacks.return_value = [postback]
        sub1 = '7a5b75c757d7c76d5c7'
        payout = 0.15
        conversion = {
            'offer_id': 1,
            'affiliate_id': 2,
            'payout': payout,
            'currency': 'USD',
            'goal_value': '2',
            'sub1': sub1,
        }
        send_postback(conversion)
        expected_url = f'http://example.com/path?sub1={sub1}&sum={payout}'
        mocked_requests.get.assert_called_with(expected_url), 'requests should be called'
        assert mocked_persist_log.called, 'persist log should be called'

    def test_goal_should_not_send_if_goal_doesnt_match(self, mocked_find_postbacks, mocked_requests, mocked_persist_log):
        postback = Postback(goal='2')
        mocked_find_postbacks.return_value = [postback]
        conversion = {
            'offer_id': 1,
            'affiliate_id': 2,
            'goal_value': '1',
        }
        send_postback(conversion)
        assert not mocked_requests.get.called, 'requests should not be called'

    def test_goal_should_send_if_goal_match(self, mocked_find_postbacks, mocked_requests, mocked_persist_log):
        postback = Postback(goal='2')
        mocked_find_postbacks.return_value = [postback]
        conversion = {
            'offer_id': 1,
            'affiliate_id': 2,
            'goal_value': '2',
        }
        send_postback(conversion)
        assert mocked_requests.get.called, 'requests should be called'
