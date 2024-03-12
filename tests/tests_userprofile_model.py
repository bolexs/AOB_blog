from django.test import TestCase
from users.models import User, Profile, UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
      user = User.objects.create(email='testuser@test.com', first_name='Test', last_name='User')
      profile = Profile.objects.create(profile_name='TestProfile')
      UserProfile.objects.create(user=user, profile=profile)


    def test_user_profile_created(self):
        user_profile = UserProfile.objects.get(user__email='testuser@test.com')
        self.assertIsNotNone(user_profile)

    
    def test_string_representation(self):
        user_profile = UserProfile.objects.get(user__email='testuser@test.com')
        self.assertEqual(str(user_profile), 'testuser@test.com TestProfile')