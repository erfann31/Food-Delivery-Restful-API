import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.http import HttpResponse
from user.views import email_verification_view
from user.models import CustomUser

class TestEmailVerificationView(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('user.repositories.custom_user_repository.CustomUserRepository.get_user_by_verification_token')
    def test_valid_token_verification(self, mock_get_user_by_token):
        mock_user = MagicMock(spec=CustomUser)
        mock_user.verified = False
        mock_get_user_by_token.return_value = mock_user

        with patch('user.repositories.token_repository.TokenRepository.check_verification_token_expired') as mock_check_token_expired, \
                patch('user.repositories.custom_user_repository.CustomUserRepository.update_user_verification_status') as mock_update_verification:
            mock_check_token_expired.return_value = False

            request = self.factory.get('/verify/token123/')
            response = email_verification_view(request, 'token123')

            self.assertEqual(response.content.decode(), "Email verified successfully")
            self.assertTrue(mock_update_verification.called)

    @patch('user.repositories.custom_user_repository.CustomUserRepository.get_user_by_verification_token')
    def test_expired_token_verification(self, mock_get_user_by_token):
        mock_user = MagicMock(spec=CustomUser)
        mock_user.verified = False
        mock_get_user_by_token.return_value = mock_user

        with patch('user.repositories.token_repository.TokenRepository.check_verification_token_expired') as mock_check_token_expired:
            mock_check_token_expired.return_value = True

            request = self.factory.get('/verify/token123/')
            response = email_verification_view(request, 'token123')

            self.assertEqual(response.content.decode(), "The verification link has expired.")
            self.assertFalse(mock_user.save.called)

    @patch('user.repositories.custom_user_repository.CustomUserRepository.get_user_by_verification_token')
    def test_already_verified_email(self, mock_get_user_by_token):
        mock_user = MagicMock(spec=CustomUser)
        mock_user.verified = True
        mock_get_user_by_token.return_value = mock_user

        request = self.factory.get('/verify/token123/')
        response = email_verification_view(request, 'token123')

        self.assertEqual(response.content.decode(), "Email already verified.")
        self.assertFalse(mock_user.save.called)

    @patch('user.repositories.custom_user_repository.CustomUserRepository.get_user_by_verification_token')
    def test_invalid_verification_token(self, mock_get_user_by_token):
        mock_get_user_by_token.return_value = None

        request = self.factory.get('/verify/token123/')
        response = email_verification_view(request, 'token123')

        self.assertEqual(response.content.decode(), "Invalid verification token.")
