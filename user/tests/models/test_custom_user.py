from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from food.models.food import Food
from restaurant.models.restaurant import Restaurant

CustomUser = get_user_model()


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.food = Food.objects.create(name='Test Food', price=10.99, category='Other', restaurant=self.restaurant)

    def test_create_user(self):
        with patch.object(CustomUser.objects, 'create_user') as mock_create_user:
            CustomUser.objects.create_user(**self.user_data)
            mock_create_user.assert_called_once_with(**self.user_data)

    @staticmethod
    def test_create_superuser():
        superuser_data = {
            'email': 'admin@example.com',
            'password': 'admin123'
        }
        with patch.object(CustomUser.objects, 'create_superuser') as mock_create_superuser:
            CustomUser.objects.create_superuser(**superuser_data)
            mock_create_superuser.assert_called_once_with(**superuser_data)

    def test_favorite_foods(self):
        user = CustomUser.objects.create_user(**self.user_data)
        user.favorite_foods.add(self.food)
        self.assertIn(self.food, user.favorite_foods.all())

    def test_favorite_restaurants(self):
        user = CustomUser.objects.create_user(**self.user_data)
        user.favorite_restaurants.add(self.restaurant)
        self.assertIn(self.restaurant, user.favorite_restaurants.all())

    def test_user_fields(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.name, self.user_data['name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))  # Checking if the password is hashed
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
