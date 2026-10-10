from io import StringIO

from django.core.mail import EmailMessage
from django.test import TestCase
from django.urls import reverse

from .mail import ReadableConsoleEmailBackend


class HealthTests(TestCase):
    def test_health(self):
        response = self.client.get(reverse('core:health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})


class IndexTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)


class ReadableConsoleEmailBackendTests(TestCase):
    def test_writes_readable_message(self):
        stream = StringIO()
        backend = ReadableConsoleEmailBackend(stream=stream)
        message = EmailMessage('Redefinição de senha', 'Olá, você!', 'a@a.com', ['b@b.com'])
        backend.send_messages([message])
        output = stream.getvalue()
        self.assertIn('Subject: Redefinição de senha', output)
        self.assertIn('Olá, você!', output)
