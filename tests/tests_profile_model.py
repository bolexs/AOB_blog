from django.test import TestCase
from users.models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        Profile.objects.create(profile_name='TestProfile')

    def test_profile_created(self):
        profile = Profile.objects.get(profile_name='TestProfile')
        self.assertIsNotNone(profile)

    def test_profile_name_max_length(self):
        profile = Profile.objects.get(profile_name='TestProfile')
        self.assertEqual(len(profile.profile_name), 11)

    def test_string_representation(self):
        profile = Profile.objects.get(profile_name='TestProfile')
        self.assertEqual(str(profile), 'TestProfile')