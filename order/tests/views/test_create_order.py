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
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id, restaurant=self.restaurant)
        self.food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=self.restaurant)

        self.endpoint = 'create_order'

    def test_create_order_valid_data(self):
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

    def test_create_order_invalid_data(self):
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

    def test_unauthorized_access(self):
        request = self.factory.post(
            self.endpoint,
            data={
                "orderItems": [{"food": 7, "quantity": 3}, {"food": 1, "quantity": 3}],
                "delivery_address": 4
            },
            format='json'
        )
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_data(self):
        request = self.factory.post(
            self.endpoint,
            data={},  # No data
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_delivery_address(self):
        request = self.factory.post(
            self.endpoint,
            data={
                'delivery_address': 9999999,  # Non-existent address ID
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_discount_code(self):
        request = self.factory.post(
            self.endpoint,
            data={
                'discount_code': 9999999,  # Non-existent discount code ID
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_data_types(self):
        request = self.factory.post(
            self.endpoint,
            data={
                'total_price': 'invalid_price',  # Incorrect data type for total_price
            },
            format='json'
        )
        force_authenticate(request, user=self.user)
        response = create_order(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
