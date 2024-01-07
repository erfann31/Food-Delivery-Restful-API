from unittest.mock import patch, Mock

from django.test import TestCase

from food.models.food import Food
from restaurant.models.restaurant import Restaurant
from user.models import CustomUser
from user.repositories.user_favorite_repository import UserFavoriteRepository


class UserFavoriteRepositoryTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.food = Food.objects.create(name='Test Food', price=10.99, category='Other', restaurant=self.restaurant)

    def test_add_favorite_restaurant(self):
        with patch.object(CustomUser.objects, 'filter') as mock_filter:
            mock_user = Mock()
            mock_user.favorite_restaurants.add = Mock()
            mock_filter.return_value.first.return_value = mock_user

            UserFavoriteRepository.add_favorite_restaurant(self.user.id, self.restaurant.id)
            mock_user.favorite_restaurants.add.assert_called_once_with(self.restaurant.id)

    def test_remove_favorite_restaurant(self):
        with patch.object(CustomUser.objects, 'filter') as mock_filter:
            mock_user = Mock()
            mock_user.favorite_restaurants.remove = Mock()
            mock_filter.return_value.first.return_value = mock_user

            UserFavoriteRepository.remove_favorite_restaurant(self.user.id, self.restaurant.id)
            mock_user.favorite_restaurants.remove.assert_called_once_with(self.restaurant.id)

    def test_add_favorite_food(self):
        with patch.object(CustomUser.objects, 'filter') as mock_filter:
            mock_user = Mock()
            mock_user.favorite_foods.add = Mock()
            mock_filter.return_value.first.return_value = mock_user

            UserFavoriteRepository.add_favorite_food(self.user.id, self.food.id)
            mock_user.favorite_foods.add.assert_called_once_with(self.food.id)

    def test_remove_favorite_food(self):
        with patch.object(CustomUser.objects, 'filter') as mock_filter:
            mock_user = Mock()
            mock_user.favorite_foods.remove = Mock()
            mock_filter.return_value.first.return_value = mock_user

            UserFavoriteRepository.remove_favorite_food(self.user.id, self.food.id)
            mock_user.favorite_foods.remove.assert_called_once_with(self.food.id)

    def test_get_user_favorites(self):
        with patch.object(CustomUser.objects, 'get') as mock_get:
            mock_user = Mock()
            mock_user.favorite_restaurants.all = Mock(return_value=[self.restaurant])
            mock_user.favorite_foods.all = Mock(return_value=[self.food])
            mock_get.return_value = mock_user

            favorite_restaurants, favorite_foods = UserFavoriteRepository.get_user_favorites(self.user.id)
            self.assertEqual(list(favorite_restaurants), [self.restaurant])
            self.assertEqual(list(favorite_foods), [self.food])
