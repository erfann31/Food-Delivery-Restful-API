import unittest
from restaurant.serializers.restaurant_serializer import RestaurantSerializer


class TestRestaurantSerializer(unittest.TestCase):

    def test_read_only_fields_id(self):
        serializer = RestaurantSerializer()
        self.assertIn('id', serializer.Meta.read_only_fields)

    def test_read_only_fields_stars(self):
        serializer = RestaurantSerializer()
        self.assertIn('stars', serializer.Meta.read_only_fields)

    def test_read_only_fields_distance(self):
        serializer = RestaurantSerializer()
        self.assertIn('distance', serializer.Meta.read_only_fields)

    def test_read_only_fields_stars_count(self):
        serializer = RestaurantSerializer()
        self.assertIn('stars_count', serializer.Meta.read_only_fields)
