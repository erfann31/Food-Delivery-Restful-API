import unittest
from unittest.mock import MagicMock
from rest_framework.exceptions import ValidationError

from food.serializers.food_serializer import FoodSerializer
from restaurant.models.restaurant import Restaurant
from restaurant.serializers.restaurant_detail_serializer import RestaurantDetailSerializer
from restaurant.serializers.restaurant_id_serializer import RestaurantIdSerializer



class TestRestaurantIdSerializer(unittest.TestCase):
    def test_valid_restaurant_id_serializer(self):
        restaurant_data = {'id': 1}  # Replace with appropriate data
        serializer = RestaurantIdSerializer(data=restaurant_data)
        self.assertTrue(serializer.is_valid())

    # Add more tests as needed for different cases related to RestaurantIdSerializer

class TestRestaurantDetailSerializer(unittest.TestCase):
    def test_valid_restaurant_detail_serializer(self):
        restaurant = Restaurant.objects.create(name='Test Restaurant')
  # Replace with appropriate restaurant instance
        serializer = RestaurantDetailSerializer(instance=restaurant)
        self.assertIsNotNone(serializer.data)

    # Add more tests as needed for different cases related to RestaurantDetailSerializer

if __name__ == '__main__':
    unittest.main()
