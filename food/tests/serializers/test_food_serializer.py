import unittest

from restaurant.models.restaurant import Restaurant
from restaurant.serializers.restaurant_detail_serializer import RestaurantDetailSerializer
from restaurant.serializers.restaurant_id_serializer import RestaurantIdSerializer


class TestRestaurantIdSerializer(unittest.TestCase):
    def test_valid_restaurant_id_serializer(self):
        restaurant = Restaurant.objects.create(name='Test Restaurant')
        restaurant_data = {'id': restaurant.id}
        serializer = RestaurantIdSerializer(data=restaurant_data)
        self.assertTrue(serializer.is_valid())


class TestRestaurantDetailSerializer(unittest.TestCase):
    def test_valid_restaurant_detail_serializer(self):
        restaurant = Restaurant.objects.create(name='Test Restaurant')
        serializer = RestaurantDetailSerializer(instance=restaurant)
        self.assertIsNotNone(serializer.data)


if __name__ == '__main__':
    unittest.main()
