import unittest

from rest_framework.exceptions import ValidationError

from food.serializers.food_create_serializer import FoodCreateSerializer
from restaurant.models.restaurant import Restaurant


class TestFoodCreateSerializer(unittest.TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.validated_data = {
            'name': 'Test Food',
            'price': 10.99,
            'category': 'Other',
            'restaurant_id': self.restaurant.id
        }

    def test_valid_serializer_data(self):
        serializer = FoodCreateSerializer(data=self.validated_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_fields(self):
        invalid_data = {
            'name': 'Test Food',
            'price': 10.99,
            'category': 'Test Category'
        }
        serializer = FoodCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('restaurant_id', serializer.errors)

    def test_invalid_min_max_delivery_times(self):
        invalid_data = {
            'restaurant_id': self.restaurant.id,
            'name': 'Test Food',
            'price': 10.99,
            'min_time_to_delivery': 60,  # Invalid: greater than max_time_to_delivery
            'max_time_to_delivery': 40,
            'category': 'Test Category'
        }
        serializer = FoodCreateSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


if __name__ == '__main__':
    unittest.main()
