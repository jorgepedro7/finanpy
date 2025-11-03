from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserManagerTests(TestCase):
    def test_create_user_requires_email(self):
        User = get_user_model()
        with self.assertRaisesMessage(ValueError, 'The email address must be provided.'):
            User.objects.create_user(email='', password='testpass123')

    def test_create_user_and_superuser(self):
        User = get_user_model()
        user = User.objects.create_user(email='regular@example.com', password='testpass123')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)

        admin = User.objects.create_superuser(email='admin@example.com', password='testpass123')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(email='broken@example.com', password='testpass123', is_staff=False)


class AuthenticationViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123')

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'email': 'newuser@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('dashboard'))
        new_user = get_user_model().objects.filter(email='newuser@example.com').first()
        self.assertIsNotNone(new_user)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_with_email_and_password(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'user@example.com',
                'password': 'testpass123',
            },
        )
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_fails_with_invalid_credentials(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'user@example.com',
                'password': 'wrongpass',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
