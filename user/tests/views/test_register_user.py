import unittest
from unittest.mock import patch, MagicMock

from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from user.models import CustomUser
from user.views import register_user, send_verification_email


class TestRegisterUserView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('user.forms.forms.UserRegistrationForm')
    def test_valid_form_data(self, mock_registration_form):
        mock_form_instance = MagicMock()
        mock_form_instance.is_valid.return_value = True
        mock_form_instance.save.return_value = CustomUser()

        mock_registration_form.return_value = mock_form_instance
        url = reverse('register')
        request = self.factory.post(url, {
            'name': 'Test User',
            'email': 'test1@example.com',
            'password': 'password123'
        })

        response = register_user(request)
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(mock_form_instance.save.called)

    @patch('user.forms.forms.UserRegistrationForm')
    def test_invalid_form_data(self, mock_registration_form):
        mock_form_instance = MagicMock()
        mock_form_instance.is_valid.return_value = False
        mock_form_instance.errors = {'email': ['Invalid email format']}

        mock_registration_form.return_value = mock_form_instance

        request = self.factory.post('/api/register/', {
            'name': 'Test User',
            'email': 'invalid_email',
            'password': 'password123'
        })

        response = register_user(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'email': ['Enter a valid email address.']})

    @patch('user.utils.email_sender.send_verification_email')
    @patch('user.utils.token_generator.generate_verification_token')
    @patch('user.utils.url_generator.get_verification_url')
    @patch('user.utils.email_sender.render_to_string')
    def test_send_verification_email(self, mock_render_to_string, mock_get_verification_url, mock_generate_verification_token, mock_send_mail):
        user = CustomUser(name='Test User', email='test@example.com')
        user.verification_token = 'mock_token'

        mock_render_to_string.return_value = 'Mock email message'
        mock_get_verification_url.return_value = 'http://example.com/verify?token=mock_token'
        mock_generate_verification_token.return_value = 'mock_token'

        send_verification_email(user)

        # self.assertTrue(mock_send_mail.called)
        self.assertEqual(len(mail.outbox), 3)


if __name__ == '__main__':
    unittest.main()
