from rest_framework.test import APITestCase

from user_profile.models import User


class ProfileTestCase(APITestCase):
    def setUp(self):
        super(ProfileTestCase, self).setUp()
        credentials = {
            'username': 'test@test.com',
            'password': '1234',
        }
        self.user = User.objects.create_user(**credentials)
        self.user.first_name = 'test username'
        self.user.save()
        # self.user.profile.phone = '+7 123 456 7890'
        # self.user.profile.skype = '@test'
        # self.user.profile.save()
        self.client.login(**credentials)

    # def test_get_profile(self):
    #     response = self.client.get('/api/profile/')
    #     self.assertEqual(200, response.status_code)
    #     # self.assertEqual(
    #     #     {
    #     #         'first_name': 'test username',
    #     #         'phone': '+7 123 456 7890',
    #     #         'skype': '@test',
    #     #     },
    #     #     response.data
    #     # )

    # def test_patch_profile(self):
    #     response = self.client.patch('/api/profile/',
    #                                  {'phone': '+1 123 456 7890'})
    #     self.assertEqual(200, response.status_code)
    #     # self.assertEqual(
    #     #     {
    #     #         'first_name': 'test username',
    #     #         'phone': '+1 123 456 7890',
    #     #         'skype': '@test',
    #     #     },
    #     #     response.data
    #     # )

    # def test_patch_first_name(self):
    #     response = self.client.patch('/api/profile/',
    #                                  {'first_name': 'test test'})
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(
    #         {
    #             'first_name': 'test test',
    #             'phone': '+7 123 456 7890',
    #             'skype': '@test',
    #         },
    #         response.data
    #     )
    #     self.assertEqual(
    #         'test test',
    #         User.objects.get(pk=self.user.pk).first_name
    #     )
