import unittest
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory

from user.repositories.token_repository import TokenRepository
from user.views import login_view


class TestTokenObtainPairView(unittest.TestCase):

    @patch('user.views.authenticate')
    def test_valid_credentials(self, mock_authenticate):
        mock_user = MagicMock()
        mock_authenticate.return_value = mock_user
        mock_user.username = 'test_user'
        mock_user.verified = True
        mock_access_token = 'mock_access_token'

        with patch('user.repositories.token_repository.TokenRepository.generate_token_for_user') as mock_generate_token:
            mock_generate_token.return_value = mock_access_token

            request = APIRequestFactory().post('/api/token/', {'email': 'test@example.com', 'password': 'test_password'})
            response = login_view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['access_token'], mock_access_token)

    @patch('user.views.authenticate')
    def test_not_verified_user(self, mock_authenticate):
        def test_not_verified_user(self, mock_authenticate):
            mock_user = MagicMock()
            mock_authenticate.return_value = mock_user
            mock_user.username = 'test_user'
            mock_user.verified = False
            mock_access_token = 'mock_access_token'

            with patch('your_app.repositories.token_repository.TokenRepository.generate_token_for_user') as mock_generate_token:
                mock_generate_token.return_value = mock_access_token

                request = APIRequestFactory().post('/api/token/', {'email': 'test@example.com', 'password': 'test_password'})
                response = login_view(request)

                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertEqual(response.data['message'], "User is not verified!")
    @patch('user.views.authenticate')
    def test_invalid_credentials(self, mock_authenticate):
        mock_authenticate.return_value = None

        request = APIRequestFactory().post('/api/token/', {'username': 'test_user', 'password': 'test_password'})
        response = login_view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'],  'this field is required!',)
        self.assertEqual(response.data['password'],  'this field is required!',)

    @patch('user.repositories.token_repository.TokenRepository.generate_token_for_user')
    def test_generate_token_for_user(self, mock_generate_token):
        mock_user = User(username='test_user')
        mock_access_token = 'mock_access_token'
        mock_generate_token.return_value = mock_access_token

        generated_token = TokenRepository.generate_token_for_user(mock_user)

        self.assertEqual(generated_token, mock_access_token)


if __name__ == '__main__':
    unittest.main()
