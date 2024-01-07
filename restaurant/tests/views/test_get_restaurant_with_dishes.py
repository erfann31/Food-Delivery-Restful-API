import unittest
from unittest.mock import patch, MagicMock

from rest_framework.test import APIRequestFactory

from restaurant.models.restaurant import Restaurant
from restaurant.views import get_restaurant_with_dishes


class TestGetRestaurantWithDishesView(unittest.TestCase):

    # @patch('restaurant.repositories.restaurant_repository.RestaurantRepository.get_restaurant_by_id')
    # @patch('food.repositories.food_repository.FoodRepository.get_foods_by_category_for_restaurant')
    # @patch('restaurant.serializers.restaurant_serializer.RestaurantSerializer')
    # def test_get_restaurant_section(self, mock_serializer, mock_get_foods_by_category_for_restaurant,
    #                                 mock_get_restaurant_by_id):
    #     # Create a mocked decimal field value to avoid the decimal.InvalidOperation error
    #     decimal_value = MagicMock()
    #     decimal_value.configure_mock(**{'__str__.return_value': '10.50'})  # Assuming a decimal field representation
    #
    #     mock_restaurant = MagicMock(stars=decimal_value, distance=decimal_value, stars_count=decimal_value)
    #     mock_serializer.return_value = MagicMock(data={'stars': '10.50', 'distance': '10.50', 'stars_count': '10.50'})
    #     mock_get_restaurant_by_id.return_value = mock_restaurant
    #     mock_get_foods_by_category_for_restaurant.return_value = {}
    #
    #     request = APIRequestFactory().get('')
    #     # restaurant = Restaurant.objects.create(name='Test Restaurant')
    #     response = get_restaurant_with_dishes(request, 1)  # Pass restaurant ID instead of the object
    #
    #     mock_get_restaurant_by_id.assert_called_once_with(1)
    #     mock_serializer.assert_called_once_with(mock_restaurant)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('restaurant', response.data)
    #     self.assertIn('dishes_by_category', response.data)

    @patch('restaurant.repositories.restaurant_repository.RestaurantRepository.get_restaurant_by_id', side_effect=Restaurant.DoesNotExist)
    def test_restaurant_not_found_section(self, mock_get_restaurant_by_id):
        request = APIRequestFactory().get('')
        response = get_restaurant_with_dishes(request, 1)

        mock_get_restaurant_by_id.assert_called_once_with(1)
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Restaurant not found')
