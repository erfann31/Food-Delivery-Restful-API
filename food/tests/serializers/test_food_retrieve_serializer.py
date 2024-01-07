import unittest
from unittest.mock import MagicMock

from food.serializers.food_retrieve_serializer import FoodRetrieveSerializer
from restaurant.models.restaurant import Restaurant
from restaurant.serializers.restaurant_detail_serializer import RestaurantDetailSerializer


class TestFoodRetrieveSerializer(unittest.TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.validated_data = {
            'name': 'Test Food',
            'price': 10.99,
            'category': 'Other',
            'restaurant_id': self.restaurant.id
        }
        self.food = MagicMock()
        self.food_serializer = FoodRetrieveSerializer(instance=self.food)


    def test_restaurant_detail_serializer_used(self):
        self.food_serializer = FoodRetrieveSerializer(instance=self.food)
        self.assertIn('restaurant', self.food_serializer.fields)
        self.assertIsInstance(self.food_serializer.fields['restaurant'], RestaurantDetailSerializer)


if __name__ == '__main__':
    unittest.main()
