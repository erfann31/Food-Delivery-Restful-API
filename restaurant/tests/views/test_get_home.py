import unittest
from unittest.mock import patch, MagicMock

from rest_framework.test import APIRequestFactory

from restaurant.views import get_home


class TestGetHomeView(unittest.TestCase):

    @patch('restaurant.serializers.restaurant_serializer.RestaurantSerializer')
    @patch('restaurant.repositories.restaurant_repository.RestaurantRepository.get_random_restaurants')
    def test_get_random_restaurants_section(self, mock_serializer, mock_get_random_restaurants):
        mock_restaurants = MagicMock()
        mock_serializer.return_value = MagicMock(data=mock_restaurants)
        mock_get_random_restaurants.return_value = mock_restaurants

        request = APIRequestFactory().get('')
        response = get_home(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('restaurants', response.data)

    @patch('food.repositories.food_repository.FoodRepository.get_random_food_categories')
    @patch('food.repositories.food_repository.FoodRepository.get_random_foods_by_category')
    @patch('food.serializers.food_serializer.FoodSerializer')
    def test_random_categories_and_foods_section(self, mock_serializer, mock_get_random_foods_by_category,
                                                 mock_get_random_food_categories):
        mock_categories = ['category1', 'category2', 'category3']
        mock_get_random_food_categories.return_value = mock_categories

        mock_foods = MagicMock()
        mock_serializer.return_value = MagicMock(data=mock_foods)
        mock_get_random_foods_by_category.return_value = mock_foods

        request = APIRequestFactory().get('')
        response = get_home(request)

        mock_get_random_food_categories.assert_called_once_with(3)
        self.assertEqual(response.status_code, 200)
        self.assertIn('food_series', response.data)
