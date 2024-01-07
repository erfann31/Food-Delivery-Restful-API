import unittest
from unittest.mock import patch

from restaurant.models.restaurant import Restaurant
from restaurant.repositories.restaurant_repository import RestaurantRepository


class TestRestaurantRepository(unittest.TestCase):

    @patch('restaurant.repositories.restaurant_repository.random.sample')
    def test_get_random_restaurants(self, mock_random_sample):
        mock_restaurants = [Restaurant(name=f"Restaurant_{i}") for i in range(5)]
        mock_random_sample.return_value = mock_restaurants[:3]  # Mocking random.sample to return 3 restaurants

        result = RestaurantRepository.get_random_restaurants(3)
        self.assertEqual(len(result), 3)  # Checking if 3 restaurants are returned
        for restaurant in result:
            self.assertIsInstance(restaurant, Restaurant)  # Checking if returned objects are instances of Restaurant

    @patch('restaurant.models.restaurant.Restaurant.objects.get')
    def test_get_restaurant_by_id(self, mock_get_restaurant_by_id):
        mock_restaurant = Restaurant(name="Test Restaurant")
        mock_get_restaurant_by_id.return_value = mock_restaurant  # Mocking Restaurant.objects.get to return a restaurant

        restaurant_id = 1
        result = RestaurantRepository.get_restaurant_by_id(restaurant_id)
        self.assertEqual(result, mock_restaurant)  # Checking if the returned restaurant matches the mocked object
