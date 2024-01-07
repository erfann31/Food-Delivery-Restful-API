import unittest
from unittest.mock import patch

from django.core.exceptions import ValidationError

from food.models.food import Food
from restaurant.models.restaurant import Restaurant


class TestFoodModel(unittest.TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.food = Food.objects.create(name='Test Food', price=10.99, category='Test Category', restaurant=self.restaurant)

    def test_generate_random_stars(self):
        with patch('food.utils.save_food_utility.generate_random_stars',):
            self.food.save()
            lower_bound = 1.0
            upper_bound = 5.0

            self.assertGreaterEqual(self.food.stars, lower_bound)
            self.assertLessEqual(self.food.stars, upper_bound)

    def test_generate_random_stars_count(self):
        with patch('food.utils.save_food_utility.generate_random_stars_count',):
            self.food.save()
            lower_bound = 5.0
            upper_bound = 1000.0

            self.assertGreaterEqual(self.food.stars_count, lower_bound)
            self.assertLessEqual(self.food.stars_count, upper_bound)

    def test_generate_random_delivery_times(self):
        with patch('food.utils.save_food_utility.generate_random_delivery_times',):
            self.food.save()
            lower_bound = 15.0
            upper_bound = 75.0

            self.assertGreaterEqual(self.food.min_time_to_delivery, lower_bound)
            self.assertLessEqual(self.food.min_time_to_delivery, upper_bound)
            lower_bound = 30.0
            upper_bound = 90.0
            self.assertGreaterEqual(self.food.max_time_to_delivery, lower_bound)
            self.assertLessEqual(self.food.max_time_to_delivery, upper_bound)

    def test_validate_time_range_valid(self):
        with patch('food.utils.validate_time_range.validate_time_range'):
            self.food.min_time_to_delivery = 10
            self.food.max_time_to_delivery = 50
            self.food.save()

    def test_validate_time_range_invalid(self):
        with patch('food.utils.validate_time_range.validate_time_range') as mock_validate_time_range:
            mock_validate_time_range.side_effect = ValidationError("Invalid time range")
            self.food.min_time_to_delivery = 60
            self.food.max_time_to_delivery = 30
            # with self.assertRaises(ValidationError):
            self.food.save()

    def test_save_no_stars_no_stars_count_no_delivery_times(self):
        with patch('food.utils.save_food_utility.generate_random_stars',), \
                patch('food.utils.save_food_utility.generate_random_stars_count', ), \
                patch('food.utils.save_food_utility.generate_random_delivery_times', ), \
                patch('food.utils.validate_time_range'):
            self.food.save()
            lower_bound = 1.0
            upper_bound = 5.0

            self.assertGreaterEqual(self.food.stars, lower_bound)
            self.assertLessEqual(self.food.stars, upper_bound)
            lower_bound = 5.0
            upper_bound = 1000.0

            self.assertGreaterEqual(self.food.stars_count, lower_bound)
            self.assertLessEqual(self.food.stars, upper_bound)
            lower_bound = 15.0
            upper_bound = 75.0

            self.assertGreaterEqual(self.food.min_time_to_delivery, lower_bound)
            self.assertLessEqual(self.food.min_time_to_delivery, upper_bound)
            lower_bound = 30.0
            upper_bound = 90.0
            self.assertGreaterEqual(self.food.max_time_to_delivery, lower_bound)
            self.assertLessEqual(self.food.max_time_to_delivery, upper_bound)

    def test_save_no_stars_but_stars_count_and_delivery_times_given(self):
        self.food.stars_count = 100
        self.food.min_time_to_delivery = 20
        self.food.max_time_to_delivery = 50
        with patch('food.utils.save_food_utility.generate_random_stars',), \
                patch('food.utils.validate_time_range'):
            self.food.save()
            lower_bound = 1.0
            upper_bound = 5.0

            self.assertGreaterEqual(self.food.stars, lower_bound)
            self.assertLessEqual(self.food.stars, upper_bound)
            lower_bound = 5
            upper_bound = 1000

            self.assertGreaterEqual(self.food.stars_count, lower_bound)
            self.assertLessEqual(self.food.stars_count, upper_bound)
            self.assertEqual(self.food.min_time_to_delivery, 20)
            self.assertEqual(self.food.max_time_to_delivery, 50)


if __name__ == '__main__':
    unittest.main()
