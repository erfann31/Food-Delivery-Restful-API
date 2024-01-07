import unittest
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from address.models.address import Address
from food.models.food import Food
from order.models.order import Order
from order.views import update_order_status
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class TestUpdateOrderStatusAPIView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))

        self.endpoint = f'update_order_status/{self.order.id}/'  # Replace with your API endpoint

    @patch('order.repositories.order_repository.OrderRepository.update_order_status')
    def test_update_order_status_success(self, mock_update_order_status):
        # Mocking update_order_status method of OrderRepository for successful status update
        mock_update_order_status.return_value = True

        # Making a GET request to update order status
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = update_order_status(request, self.order.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order status updated to Completed')
        # Add assertions based on the expected behavior for a successful update

    @patch('order.repositories.order_repository.OrderRepository.update_order_status')
    def test_update_order_status_failure(self, mock_update_order_status):
        # Mocking update_order_status method of OrderRepository for order not found
        mock_update_order_status.return_value = False

        # Making a GET request to update order status for a non-existent order
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = update_order_status(request, self.order.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Order not found')
        # Add assertions based on the expected behavior for a failed update


if __name__ == '__main__':
    unittest.main()
