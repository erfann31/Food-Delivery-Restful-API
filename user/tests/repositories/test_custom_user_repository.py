from unittest.mock import patch

from django.test import TestCase

from user.models import CustomUser
from user.repositories.custom_user_repository import CustomUserRepository


class CustomUserRepositoryTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.updated_data = {'name': 'Jane Doe', 'email': 'jane@example.com'}

    def test_get_user_by_id(self):
        with patch.object(CustomUser.objects, 'get') as mock_get:
            CustomUserRepository.get_user_by_id(self.user.id)
            mock_get.assert_called_once_with(pk=self.user.id)

    def test_update_user_profile(self):
        with patch.object(CustomUser, 'save') as mock_save:
            CustomUserRepository.update_user_profile(self.user, self.updated_data)
            self.assertEqual(self.user.name, 'Jane Doe')
            self.assertEqual(self.user.email, 'jane@example.com')
            mock_save.assert_called_once()

    @staticmethod
    def test_get_user_by_email():
        with patch.object(CustomUser.objects, 'get') as mock_get:
            CustomUserRepository.get_user_by_email('john@example.com')
            mock_get.assert_called_once_with(email='john@example.com')

    @staticmethod
    def test_get_user_by_verification_token():
        with patch.object(CustomUser.objects, 'get') as mock_get:
            CustomUserRepository.get_user_by_verification_token('verification_token')
            mock_get.assert_called_once_with(verification_token='verification_token')

    @staticmethod
    def test_get_user_by_reset_password_token():
        with patch.object(CustomUser.objects, 'get') as mock_get:
            CustomUserRepository.get_user_by_reset_password_token('reset_password_token')
            mock_get.assert_called_once_with(password_reset_token='reset_password_token')
