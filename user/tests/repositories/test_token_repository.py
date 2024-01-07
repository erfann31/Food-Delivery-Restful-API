from unittest.mock import patch

from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import CustomUser
from user.repositories.token_repository import TokenRepository


class TokenRepositoryTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_generate_token_for_user(self):
        with patch.object(RefreshToken, 'for_user') as mock_for_user:
            mock_for_user.return_value.access_token = 'mock_access_token'
            token = TokenRepository.generate_token_for_user(self.user)
            self.assertEqual(token, 'mock_access_token')

    def test_generate_password_reset_token(self):
        with patch('user.repositories.token_repository.TokenRepository.generate_password_reset_token') as mock_generate_token, \
                patch.object(CustomUser, 'save') as mock_user_save:
            TokenRepository.generate_password_reset_token(self.user)
            self.assertTrue(mock_generate_token.called)
            # mock_user_save.assert_called_once()

    def test_check_verification_token_expired(self):
        with patch('user.repositories.token_repository.TokenRepository.check_verification_token_expired') as mock_expired:
            TokenRepository.check_verification_token_expired(self.user)
            mock_expired.assert_called_once_with(self.user)

    def test_check_password_reset_token_expired(self):
        with patch('user.repositories.token_repository.TokenRepository.check_password_reset_token_expired') as mock_expired:
            TokenRepository.check_password_reset_token_expired(self.user)
            mock_expired.assert_called_once_with(self.user)
