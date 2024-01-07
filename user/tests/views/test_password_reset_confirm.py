import unittest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory
from rest_framework import status
from user.views import password_reset_request
from user.models import CustomUser

class TestPasswordResetRequestView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('user.repositories.custom_user_repository.CustomUserRepository.get_user_by_email')
    @patch('user.repositories.token_repository.TokenRepository.generate_password_reset_token')
    @patch('user.utils.email_sender.send_password_reset_email')
    def test_password_reset_request_successful(self, mock_send_email, mock_generate_token, mock_get_user_by_email):
        mock_user = MagicMock(spec=CustomUser)
        mock_get_user_by_email.return_value = mock_user

        request = self.factory.post('/password/reset/', {'email': 'test@example.com'})
        response = password_reset_request(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "Password reset link sent to your email."})
        self.assertTrue(mock_generate_token.called)
        self.assertFalse(mock_send_email.called)

    @patch('user.repositories.custom_user_repository.CustomUserRepository.get_user_by_email')
    def test_password_reset_request_user_not_found(self, mock_get_user_by_email):
        mock_get_user_by_email.return_value = None

        request = self.factory.post('/password/reset/', {'email': 'nonexistent@example.com'})
        response = password_reset_request(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'message': "User not found."})
