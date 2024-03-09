from django.test import TestCase
from users.models import User, Profile, UserProfile




class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='testuser@test.com', first_name='Test', last_name='User')

    def test_email_unique(self):
        user = User.objects.get(email='testuser@test.com')
        self.assertIsNotNone(user)
        with self.assertRaises(Exception):
            User.objects.create(email='testuser@test.com', first_name='Test', last_name='User')

    
    def test_first_last_name_max_length(self):
        user = User.objects.get(email='testuser@test.com')
        self.assertEqual(len(user.first_name), 4)
        self.assertEqual(len(user.last_name), 4)


    def test_is_staff_default(self):
        user = User.objects.get(email='testuser@test.com')
        self.assertFalse(user.is_staff)

    def test_is_active_default(self):
        user = User.objects.get(email='testuser@test.com')
        self.assertFalse(user.is_active)

    def test_username_field(self):
        user = User.objects.get(email='testuser@test.com')
        self.assertEqual(user.USERNAME_FIELD, 'email')

    def test_string_representation(self):
        user = User.objects.get(email='testuser@test.com')
        self.assertEqual(str(user), 'testuser@test.com')
