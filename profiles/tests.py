from django.contrib.auth import get_user_model
from django.test import TestCase

from profiles.models import Profile


class ProfileSignalTests(TestCase):
    def test_profile_created_when_user_is_created(self):
        user = get_user_model().objects.create_user(email='profile@example.com', password='testpass123')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(str(user.profile), f'Profile for {user.email}')
