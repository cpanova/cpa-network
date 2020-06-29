from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class AffiliateTestCase(APITestCase):
    list_url = '/network/affiliates/'
    retrieve_url = '/network/affiliates/{}/'

    def get_retrieve_url(self, id_):
        return self.retrieve_url.format(id_)

    def setUp(self):
        super(AffiliateTestCase, self).setUp()
        self.credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.staff_credentials = {
            'username': 'staff',
            'password': '1234',
        }
        self.staff = (
            get_user_model().objects
            .create_user(is_staff=True, **self.staff_credentials)
        )

    def test_not_staff_cant_access_list(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.list_url)
        self.assertEqual(403, response.status_code)

    def test_staff_can_access_list(self):
        self.client.login(**self.staff_credentials)
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('username', response.data[0])
        self.assertIn('email', response.data[0])

    def test_retrieve(self):
        self.client.login(**self.staff_credentials)
        response = self.client.get(self.get_retrieve_url(self.user.id))
        self.assertEqual(200, response.status_code)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
