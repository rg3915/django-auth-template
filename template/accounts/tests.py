import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(email='ana@email.com', password='s3nh4-forte!')
        self.assertEqual(user.email, 'ana@email.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('s3nh4-forte!'))

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='s3nh4-forte!')

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@email.com', password='s3nh4-forte!')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_has_no_username(self):
        self.assertFalse(hasattr(User, 'username') and User.username is not None)

    def test_str_is_email(self):
        user = User.objects.create_user(email='ana@email.com', password='s3nh4-forte!')
        self.assertEqual(str(user), 'ana@email.com')


class LoginTests(TestCase):
    def setUp(self):
        User.objects.create_user(email='ana@email.com', password='s3nh4-forte!')

    def test_login_with_email(self):
        response = self.client.post(
            reverse('login'), {'username': 'ana@email.com', 'password': 's3nh4-forte!'}
        )
        self.assertRedirects(response, reverse('core:index'))

    def test_login_ignores_case(self):
        response = self.client.post(
            reverse('login'), {'username': 'Ana@Email.com', 'password': 's3nh4-forte!'}
        )
        self.assertRedirects(response, reverse('core:index'))

    def test_login_wrong_password(self):
        response = self.client.post(
            reverse('login'), {'username': 'ana@email.com', 'password': 'errada'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class SignupTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(reverse('signup'), {
            'email': 'bia@email.com',
            'first_name': 'Bia',
            'last_name': 'Souza',
            'password1': 's3nh4-forte!',
            'password2': 's3nh4-forte!',
        })
        self.assertRedirects(response, reverse('core:index'))
        self.assertTrue(User.objects.filter(email='bia@email.com').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class ProfileTests(TestCase):
    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_updates_name(self):
        user = User.objects.create_user(email='ana@email.com', password='s3nh4-forte!')
        self.client.force_login(user)
        self.client.post(reverse('profile'), {'first_name': 'Ana', 'last_name': 'Lima'})
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Ana')


class PasswordResetTests(TestCase):
    def test_full_password_reset_flow(self):
        User.objects.create_user(email='ana@email.com', password='senha-antiga!')

        # 1. Pede o link
        response = self.client.post(reverse('password_reset'), {'email': 'ana@email.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Redefinição de senha', mail.outbox[0].subject)

        # 2. Abre o link do e-mail
        link = re.search(r'http://testserver(/accounts/reset/\S+)', mail.outbox[0].body).group(1)
        response = self.client.get(link, follow=True)
        self.assertTrue(response.context['validlink'])

        # 3. Define a senha nova
        response = self.client.post(response.redirect_chain[-1][0], {
            'new_password1': 'senha-nova-123!',
            'new_password2': 'senha-nova-123!',
        })
        self.assertRedirects(response, reverse('password_reset_complete'))

        # 4. Entra com a senha nova
        self.assertTrue(self.client.login(username='ana@email.com', password='senha-nova-123!'))
