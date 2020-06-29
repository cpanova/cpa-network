from django.test import TestCase

from user_profile.models import Profile, User


class SignalTestCase(TestCase):
    def test_create_profile(self):
        user = User.objects.create_user(username='test@test.com')
        self.assertEqual(
            1,
            Profile.objects.filter(user=user).count()
        )
