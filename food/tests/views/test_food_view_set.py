from rest_framework import status
from rest_framework.test import APITestCase

from food.models.food import Food
from food.views import FoodViewSet
from restaurant.models.restaurant import Restaurant


class FoodViewSetTests(APITestCase):
    def setUp(self):
        self.view = FoodViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'update', 'delete': 'destroy'})
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.food = Food.objects.create(name='Test Food', restaurant=self.restaurant, price=1400, max_time_to_delivery=80, min_time_to_delivery=60)

    def test_list_foods(self):
        response = self.client.get('/foods/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_food(self):
        response = self.client.get(f'/foods/{self.food.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_food(self):
        data = {"name": "New Food", "category": "Pizza", "price": 15.0, "restaurant_id": 1, "min_time_to_delivery": 74, "max_time_to_delivery": 89, }
        response = self.client.post('/foods/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_food(self):
        data = {'name': 'Updated Food'}
        response = self.client.patch(f'/foods/{self.food.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_food(self):
        response = self.client.delete(f'/foods/{self.food.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)