import unittest
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from user.views import get_user_favorites

User = get_user_model()


class TestGetUserFavoritesView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(name='test', password='test', email='test@example.com')

    # @patch('user.repositories.user_favorite_repository.UserFavoriteRepository.get_user_favorites')
    # def test_get_user_favorites_success(self, mock_get_user_favorites):
    #     favorite_restaurants = [MagicMock(), MagicMock()]
    #     favorite_foods = [MagicMock(), MagicMock()]
    #
    #     mock_get_user_favorites.return_value = (favorite_restaurants, favorite_foods)
    #     url = reverse('get_user_favorites')
    #     request = self.factory.get(url)
    #     force_authenticate(request, user=self.user)
    #     response = get_user_favorites(request)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     mock_get_user_favorites.assert_called_once_with(self.user.id)

    @patch('user.repositories.user_favorite_repository.UserFavoriteRepository.get_user_favorites')
    def test_get_user_favorites_user_not_found(self, mock_get_user_favorites):
        mock_get_user_favorites.return_value = (None, None)
        url = reverse('get_user_favorites')

        request = self.factory.get(url)
        # force_authenticate(request, user=self.user)
        response = get_user_favorites(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})
