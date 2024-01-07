import unittest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response

from user.repositories.token_repository import TokenRepository
from user.views import TokenObtainPairView


class TestTokenObtainPairView(unittest.TestCase):

    @patch('user.views.authenticate')
    def test_valid_credentials(self, mock_authenticate):
        mock_user = MagicMock()
        mock_authenticate.return_value = mock_user
        mock_user.username = 'test_user'
        mock_access_token = 'mock_access_token'

        with patch('user.repositories.token_repository.TokenRepository.generate_token_for_user') as mock_generate_token:
            mock_generate_token.return_value = mock_access_token

            request = APIRequestFactory().post('/api/token/', {'username': 'test_user', 'password': 'test_password'})
            response = TokenObtainPairView.as_view()(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['access_token'], mock_access_token)

    @patch('user.views.authenticate')
    def test_invalid_credentials(self, mock_authenticate):
        mock_authenticate.return_value = None

        request = APIRequestFactory().post('/api/token/', {'username': 'test_user', 'password': 'test_password'})
        response = TokenObtainPairView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid credentials')

    @patch('user.repositories.token_repository.TokenRepository.generate_token_for_user')
    def test_generate_token_for_user(self, mock_generate_token):
        mock_user = User(username='test_user')
        mock_access_token = 'mock_access_token'
        mock_generate_token.return_value = mock_access_token

        generated_token = TokenRepository.generate_token_for_user(mock_user)

        self.assertEqual(generated_token, mock_access_token)


if __name__ == '__main__':
    unittest.main()
