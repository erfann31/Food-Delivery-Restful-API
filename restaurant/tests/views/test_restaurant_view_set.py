from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models.restaurant import Restaurant
from restaurant.views import RestaurantViewSet


class RestaurantViewSetTests(APITestCase):
    def setUp(self):
        self.view = RestaurantViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'update', 'delete': 'destroy'})
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', category='Burger')

    def test_list_restaurants(self):
        response = self.client.get('/restaurant/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_restaurant(self):
        response = self.client.get(f'/restaurant/{self.restaurant.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_restaurant(self):
        data = {'name': 'New Restaurant', 'category': 'Pizza', 'address': 1}
        response = self.client.post('/restaurant/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_restaurant(self):
        data = {'name': 'Updated Name'}
        response = self.client.patch(f'/restaurant/{self.restaurant.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_restaurant(self):
        response = self.client.delete(f'/restaurant/{self.restaurant.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
