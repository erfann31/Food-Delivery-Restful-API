import unittest
from unittest.mock import patch, MagicMock

from consts.constants import CATEGORY_CHOICES
from food.models.food import Food
from food.repositories.food_repository import FoodRepository
from restaurant.models.restaurant import Restaurant


class TestFoodRepository(unittest.TestCase):

    def setUp(self):
        self.food_instance = Food.objects.create(name="Test Food", price=10.99, category="Other", restaurant_id=1)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

    @patch('food.models.food.Food.objects')
    def test_get_food_by_id(self, mock_food_objects):
        food_id = 1
        mock_food_objects.get.return_value = self.food_instance

        result = FoodRepository.get_food_by_id(food_id)

        self.assertEqual(result, self.food_instance)
        mock_food_objects.get.assert_called_once_with(pk=food_id)

    @patch('food.models.food.Food.objects')
    def test_get_random_foods_by_category(self, mock_food_objects):
        category = "Other"
        count = 5
        mock_food_objects.filter.return_value = [self.food_instance] * count

        result = FoodRepository.get_random_foods_by_category(category, count)

        self.assertEqual(len(result), count)
        mock_food_objects.filter.assert_called_once_with(category=category)


    @patch('food.models.food.Food.save')
    @patch('food.utils.save_food_utility.generate_random_stars')
    @patch('food.utils.save_food_utility.generate_random_stars_count')
    @patch('food.utils.save_food_utility.generate_random_delivery_times')
    @patch('food.utils.validate_time_range.validate_time_range')
    def test_save_food_with_random_attrs(self, mock_validate_time_range, mock_generate_random_delivery_times,
                                         mock_generate_random_stars_count, mock_generate_random_stars, mock_save):
        name = "New Food"
        price = 15.99
        category = "Other"
        restaurant = self.restaurant

        result = FoodRepository.save_food_with_random_attrs(name, price, category, restaurant)

        self.assertEqual(result.name, name)
        self.assertEqual(result.price, price)
        lower_bound = 1.0
        upper_bound = 5.0

        self.assertGreaterEqual(result.stars, lower_bound)
        self.assertLessEqual(result.stars, upper_bound)
        lower_bound = 5.0
        upper_bound = 1000.0

        self.assertGreaterEqual(result.stars_count, lower_bound)
        self.assertLessEqual(result.stars, upper_bound)
        lower_bound = 15.0
        upper_bound = 75.0

        self.assertGreaterEqual(result.min_time_to_delivery, lower_bound)
        self.assertLessEqual(result.min_time_to_delivery, upper_bound)
        lower_bound = 30.0
        upper_bound = 90.0
        self.assertGreaterEqual(result.max_time_to_delivery, lower_bound)
        self.assertLessEqual(result.max_time_to_delivery, upper_bound)


if __name__ == '__main__':
    unittest.main()
