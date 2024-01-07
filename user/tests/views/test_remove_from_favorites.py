import unittest
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from user.views import remove_from_favorites

User = get_user_model()


class TestRemoveFromFavoritesView(unittest.TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(name='test', password='test', email='test@example.com')

    @patch('user.repositories.user_favorite_repository.UserFavoriteRepository.remove_favorite_restaurant')
    @patch('user.repositories.user_favorite_repository.UserFavoriteRepository.remove_favorite_food')
    def test_successful_remove_from_favorites(self, mock_remove_favorite_food, mock_remove_favorite_restaurant):
        request = self.factory.post(
            '/remove_from_favorites/',
            {'restaurant_ids': [1, 2, 3], 'food_ids': [4, 5]},
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = remove_from_favorites(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Removed from favorites successfully'})
        self.assertTrue(mock_remove_favorite_restaurant.call_count, 3)
        self.assertTrue(mock_remove_favorite_food.call_count, 2)

    def test_missing_data(self):
        request = self.factory.post('/remove_from_favorites/', {}, format='json')
        force_authenticate(request, user=self.user)
        response = remove_from_favorites(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'error': 'At least one restaurant_ids or food_ids field is required'}
        )

    def test_no_ids_provided(self):
        request = self.factory.post('/remove_from_favorites/', {'restaurant_ids': [], 'food_ids': []}, format='json')
        force_authenticate(request, user=self.user)
        response = remove_from_favorites(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'At least one restaurant_ids or food_ids field is required'})

    @patch('user.repositories.custom_user_repository.CustomUser.objects.filter')
    def test_user_not_found(self, mock_user_filter):
        mock_user_filter.return_value.first.return_value = None
        url = '/remove_from_favorites/'
        request = self.factory.post(
            url,
            {'restaurant_ids': [3], 'food_ids': [4, 5]},
            format='json'
        )
        # force_authenticate(request, user=self.user)
        response = remove_from_favorites(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})
