from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from rest_framework import status, serializers
from rest_framework.test import force_authenticate

from address.models.address import Address
from address.views import edit_or_delete_address

User = get_user_model()


class TestEditOrDeleteAddressView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@example.com')

    def test_edit_address_valid_data(self):
        address = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')

        request = self.factory.patch(f'/edit_or_delete_address/{address.id}/', {'city': 'New City'}, content_type='application/json')
        force_authenticate(request, user=self.user)

        with patch('address.views.AddressRepository.update_address') as mock_update_address:
            mock_update_address.return_value = {'city': 'New City'}  # Simulate updated data

            response = edit_or_delete_address(request, address.id)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_address_invalid_data(self):
        address = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')

        request = self.factory.patch(f'/edit_or_delete_address/{address.id}/', {'city': ''}, content_type='application/json')
        force_authenticate(request, user=self.user)

        with patch('address.repositories.address_repository.AddressRepository.update_address') as mock_update_address:
            mock_update_address.side_effect = serializers.ValidationError('City cannot be empty')

            response = edit_or_delete_address(request, address.id)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_address(self):
        address = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')

        request = self.factory.delete(f'/edit_or_delete_address/{address.id}/')
        force_authenticate(request, user=self.user)

        with patch('address.repositories.address_repository.AddressRepository.delete_address'):
            response = edit_or_delete_address(request, address.id)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_address_not_found(self):
        non_existing_address_id = 9999

        request = self.factory.patch(f'/edit_or_delete_address/{non_existing_address_id}/', {'city': 'New City'}, content_type='application/json')
        force_authenticate(request, user=self.user)

        response = edit_or_delete_address(request, non_existing_address_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
