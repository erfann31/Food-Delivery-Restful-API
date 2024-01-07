import unittest
from unittest.mock import patch

from restaurant.models.restaurant import Restaurant


class TestRestaurantModel(unittest.TestCase):

    def test_generate_random_stars(self):
        restaurant = Restaurant.objects.create(name='Test Restaurant', category='Test Category', address='Test Address')
        restaurant.save()
        self.assertIsNotNone(restaurant.stars)

    def test_generate_random_stars_count(self):
        restaurant = Restaurant.objects.create(name='Test Restaurant', category='Test Category', address='Test Address')
        restaurant.save()
        self.assertIsNotNone(restaurant.stars_count)

    def test_generate_random_distance(self):
        restaurant = Restaurant.objects.create(name='Test Restaurant', category='Test Category', address='Test Address')
        restaurant.save()
        self.assertIsNotNone(restaurant.distance)

    @patch('restaurant.utils.save_restaurant_utility.generate_random_stars', return_value=4.5)
    def test_save_method_with_generate_random_stars(self, mock_generate_random_stars):
        restaurant = Restaurant.objects.create(name='Test Restaurant', category='Test Category', address='Test Address')
        restaurant.save()
        lower_bound = 1.0
        upper_bound = 5.0

        self.assertGreaterEqual(restaurant.stars, lower_bound)
        self.assertLessEqual(restaurant.stars, upper_bound)

    @patch('restaurant.utils.save_restaurant_utility.generate_random_stars_count', return_value=100)
    def test_save_method_with_generate_random_stars_count(self, mock_generate_random_stars_count):
        restaurant = Restaurant.objects.create(name='Test Restaurant', category='Test Category', address='Test Address')
        restaurant.save()
        lower_bound = 500.0
        upper_bound = 10000.0

        self.assertGreaterEqual(restaurant.stars_count, lower_bound)
        self.assertLessEqual(restaurant.stars_count, upper_bound)

    @patch('restaurant.utils.save_restaurant_utility.generate_random_distance', return_value=5.0)
    def test_save_method_with_generate_random_distance(self, mock_generate_random_distance):
        restaurant = Restaurant.objects.create(name='Test Restaurant', category='Test Category', address='Test Address')
        restaurant.save()
        lower_bound = 0.3
        upper_bound = 5

        self.assertGreaterEqual(restaurant.distance, lower_bound)
        self.assertLessEqual(restaurant.distance, upper_bound)
