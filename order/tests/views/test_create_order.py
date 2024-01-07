import unittest
from unittest import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from address.models.address import Address
from food.models.food import Food
from order.models.order import Order
from order.views import create_order  # Assuming your view function is in order/views.py
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class TestCreateOrderAPIView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))

        self.endpoint = 'create_order'  # Replace with your API endpoint

    def test_create_order_valid_data(self):
        # Mocking a valid POST request with valid data
        request = self.factory.post(
            self.endpoint,
            data={
                "orderItems": [{"food": 7, "quantity": 3}, {"food": 1, "quantity": 3}],
                "delivery_address": 4
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add assertions based on the expected behavior

    def test_create_order_invalid_data(self):
        # Mocking a POST request with invalid data
        request = self.factory.post(
            self.endpoint,
            data={
                # "orderItems": [{"food": 7, "quantity": 3}, {"food": 1, "quantity": 3}],
                "delivery_address": 4
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions based on the expected behavior

    def test_unauthorized_access(self):
        # Testing unauthorized access by providing no authentication
        request = self.factory.post(
            self.endpoint,
            data={
                # Your valid data for creating an order
            },
            format='json'
        )
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Add assertions based on the expected behavior

    def test_missing_data(self):
        # Testing the case of missing data in the request
        request = self.factory.post(
            self.endpoint,
            data={},  # No data provided, which is required for creating an order
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions based on the expected behavior

    def test_invalid_delivery_address(self):
        # Testing invalid delivery address (e.g., non-existent address ID)
        request = self.factory.post(
            self.endpoint,
            data={
                # Valid data for creating an order, but with an invalid delivery address ID
                'delivery_address': 9999999,  # Non-existent address ID
                # Other required data
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions based on the expected behavior

    def test_invalid_discount_code(self):
        # Testing with an invalid discount code (e.g., non-existent discount code ID)
        request = self.factory.post(
            self.endpoint,
            data={
                # Valid data for creating an order, but with an invalid discount code ID
                'discount_code': 9999999,  # Non-existent discount code ID
                # Other required data
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions based on the expected behavior (maybe ignoring the discount code)

    def test_incorrect_data_types(self):
        # Testing with incorrect data types for certain fields
        request = self.factory.post(
            self.endpoint,
            data={
                # Incorrect data types for some fields, e.g., providing a string for a numeric field
                'total_price': 'invalid_price',  # Incorrect data type for total_price
                # Other required data
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions based on the expected behavior


if __name__ == '__main__':
    unittest.main()
