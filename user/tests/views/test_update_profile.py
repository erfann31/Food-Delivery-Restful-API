from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()
class UpdateProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User')
        self.access_token = str(AccessToken.for_user(self.user))

    def test_update_profile_name_success(self):
        request_data = {'name': 'Updated Name'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = self.user

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.patch(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Updated Name')

            user = User.objects.get(email='test@example.com')
            self.assertEqual(user.name, 'Updated Name')

    def test_update_profile_mobile_number_success(self):
        request_data = {'mobile_number': '1234567890'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = self.user

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.patch(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['mobile_number'], '1234567890')

            user = User.objects.get(email='test@example.com')
            self.assertEqual(user.mobile_number, '1234567890')

    def test_update_profile_photo_success(self):
        request_data = {'photo': 'test_photo.jpg'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = self.user

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}  # Replace self.access_token with your actual token
            response = self.client.patch(url, request_data, format='json', **headers)
            # print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['photo'], '/test_photo.jpg')

            # # Check if the user's photo is updated in the database
            # user = User.objects.get(email='test@example.com')
            # self.assertEqual(user.photo, '/test_photo.jpg')

    def test_update_profile_invalid_user_id(self):
        request_data = {'name': 'Updated Name'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.side_effect = User.DoesNotExist

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.patch(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

