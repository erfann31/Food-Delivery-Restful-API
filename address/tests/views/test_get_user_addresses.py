from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from address.views import get_user_addresses

User = get_user_model()


class TestGetUserAddressesView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(name='test', password='test', email='test@example.com')

    def test_get_user_addresses_success(self):
        addresses_data = [
            {'street_address': '123 Main St', 'city': 'Anytown', 'state': 'ABC', 'zipcode': '12345'},
            {'street_address': '456 Elm St', 'city': 'Othertown', 'state': 'XYZ', 'zipcode': '54321'}
        ]
        expected_response = addresses_data

        request = self.factory.get('/get_user_addresses/')
        force_authenticate(request, user=self.user)

        with patch('address.repositories.address_repository.AddressRepository.get_user_addresses') as mock_get_user_addresses:
            mock_get_user_addresses.return_value = expected_response

            response = get_user_addresses(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, expected_response)

    def test_get_user_addresses_empty(self):
        expected_response = []
        url = reverse('get_user_addresses')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        with patch('address.repositories.address_repository.AddressRepository.get_user_addresses') as mock_get_user_addresses:
            mock_get_user_addresses.return_value = expected_response

            response = get_user_addresses(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, expected_response)
