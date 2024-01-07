import unittest
from unittest import TestCase
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from address.models.address import Address
from food.models.food import Food
from order.models.order import Order
from order.views import get_user_orders  # Assuming your view function is in order/views.py
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class TestGetUserOrdersAPIView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))

        self.endpoint = 'get_user_orders'  # Replace with your API endpoint

    @patch('order.repositories.order_repository.OrderRepository.get_completed_orders')
    def test_get_completed_orders(self, mock_get_completed_orders):
        # Mocking get_completed_orders method of OrderRepository
        mock_completed_orders = []  # Mock completed orders data
        mock_get_completed_orders.return_value = mock_completed_orders

        # Making a GET request to get completed orders
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = get_user_orders(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on the expected behavior of completed orders

    @patch('order.repositories.order_repository.OrderRepository.get_ongoing_orders')
    def test_get_ongoing_orders(self, mock_get_ongoing_orders):
        # Mocking get_ongoing_orders method of OrderRepository
        mock_ongoing_orders = []  # Mock ongoing orders data
        mock_get_ongoing_orders.return_value = mock_ongoing_orders

        # Making a GET request to get ongoing orders
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = get_user_orders(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on the expected behavior of ongoing orders


if __name__ == '__main__':
    unittest.main()
