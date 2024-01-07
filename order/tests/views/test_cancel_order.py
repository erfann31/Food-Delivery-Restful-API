import unittest
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from address.models.address import Address
from order.models.order import Order
from order.views import cancel_order

User = get_user_model()

class TestCancelOrderAPIView(TestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.order_id = self.order.id
        self.endpoint = f'/cancel_order/{self.order_id}/'  # Replace with your API endpoint

    @patch('order.repositories.order_repository.OrderRepository.cancel_order')
    def test_cancel_order_success(self, mock_cancel_order):
        # Mocking cancel_order method of OrderRepository for successful cancellation
        mock_cancel_order.return_value = True

        # Making a GET request to cancel an order
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = cancel_order(request, self.order_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order cancelled successfully!')
        # Add assertions based on the expected behavior for a successful cancellation

    @patch('order.repositories.order_repository.OrderRepository.cancel_order')
    def test_cancel_order_failure(self, mock_cancel_order):
        # Mocking cancel_order method of OrderRepository for order not found
        mock_cancel_order.return_value = False

        # Making a GET request to cancel a non-existent order
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = cancel_order(request, self.order_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Order not found')
        # Add assertions based on the expected behavior for a failed cancellation


if __name__ == '__main__':
    unittest.main()