import unittest
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from address.models.address import Address
from discount_code.models.discount_code import DiscountCode
from order.models.order import Order
from order.views import add_discount_code

User = get_user_model()


class TestAddDiscountCodeAPIView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.order_id = self.order.id

        self.endpoint = f'/add_discount_code/{self.order_id}/'  # Replace with your API endpoint

    @patch('order.repositories.order_repository.OrderRepository.apply_discount_code')
    @patch('discount_code.repositories.discount_code_repository.DiscountCodeRepository.get_discount_code_by_text')
    def test_add_discount_code_valid(self, mock_get_discount_code_by_text, mock_apply_discount_code):
        # Mocking get_discount_code_by_text method of DiscountCodeRepository for a valid discount code
        mock_discount_code = DiscountCode(code_text='VALIDCODE', discount_percent=10, is_active=True)
        mock_get_discount_code_by_text.return_value = mock_discount_code

        # Mocking apply_discount_code method of OrderRepository
        mock_order = Order(total_price=100)  # Replace with a mock order object
        mock_apply_discount_code.return_value = None

        # Making a POST request to add a discount code
        request = self.factory.post(self.endpoint, {'discount_code': 'VALIDCODE'})
        force_authenticate(request, user=self.user)
        response = add_discount_code(request, self.order_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on the expected behavior for a valid discount code

    @patch('discount_code.repositories.discount_code_repository.DiscountCodeRepository.get_discount_code_by_text')
    def test_add_discount_code_invalid(self, mock_get_discount_code_by_text):
        # Mocking get_discount_code_by_text method of DiscountCodeRepository for an invalid discount code
        mock_get_discount_code_by_text.return_value = None

        # Making a POST request to add an invalid discount code
        request = self.factory.post(self.endpoint, {'discount_code': 'INVALIDCODE'})
        force_authenticate(request, user=self.user)
        response = add_discount_code(request, self.order_id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add assertions based on the expected behavior for an invalid discount code


if __name__ == '__main__':
    unittest.main()
