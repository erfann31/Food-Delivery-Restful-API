import unittest

from restaurant.models.restaurant import Restaurant
from restaurant.serializers.restaurant_detail_serializer import RestaurantDetailSerializer


class TestRestaurantDetailSerializer(unittest.TestCase):

    def test_detail_serializer_model(self):
        serializer = RestaurantDetailSerializer()
        self.assertEqual(serializer.Meta.model, Restaurant)

    def test_detail_serializer_all_fields(self):
        serializer = RestaurantDetailSerializer()
        self.assertEqual(serializer.Meta.fields, '__all__')
