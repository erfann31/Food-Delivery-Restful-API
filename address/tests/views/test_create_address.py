from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import force_authenticate

from address.models.address import Address
from address.views import create_address

User = get_user_model()


class TestCreateAddressView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(name='test', password='test', email='test@example.com')

    def test_create_address_valid_data(self):
        request = self.factory.post('/create_address/', {'street_address': '123 Main St', 'city': 'Anytown', 'state': 'ABC', 'zipcode': '12345'})
        force_authenticate(request, user=self.user)

        with patch('address.views.create_address') as mock_create_address:
            mock_create_address.return_value = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')

            response = create_address(request)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_address_invalid_data(self):
        request = self.factory.post('/create_address/', {'street_address': '123 Main St', 'city': 'Anytown', 'state': 'ABC'})
        force_authenticate(request, user=self.user)

        with patch('address.views.create_address') as mock_create_address:
            mock_create_address.return_value = None

            response = create_address(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_address_authentication_failure(self):
        request = self.factory.post('/create_address/', {'street_address': '123 Main St', 'city': 'Anytown', 'state': 'ABC', 'zipcode': '12345'})

        response = create_address(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
