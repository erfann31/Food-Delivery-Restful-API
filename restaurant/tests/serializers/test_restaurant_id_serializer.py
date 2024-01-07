import unittest

from restaurant.models.restaurant import Restaurant
from restaurant.serializers.restaurant_id_serializer import RestaurantIdSerializer


class TestRestaurantIdSerializer(unittest.TestCase):

    def test_id_serializer_fields(self):
        serializer = RestaurantIdSerializer()
        self.assertEqual(serializer.Meta.model, Restaurant)
        self.assertEqual(serializer.Meta.fields, ['id'])
