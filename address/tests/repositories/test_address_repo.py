import unittest
from unittest.mock import patch

from django.contrib.auth import get_user_model

from address.models.address import Address
from address.repositories.address_repository import AddressRepository

User = get_user_model()


class TestAddressRepository(unittest.TestCase):

    def setUp(self):
        User.objects.filter(email='test@example.com').delete()
        self.user = User.objects.create(name='test', password='test', email='test@example.com')

    # def test_create_address(self):
    #     data = {'street_address': '123 Main St', 'city': 'Anytown', 'state': 'ABC', 'zipcode': '12345'}
    #     with patch('address.models.address.Address') as mock_address_model:
    #         AddressRepository.create_address(data, self.user)
    #         mock_address_model.assert_called_once_with(user=self.user, **data)

    def test_get_address_by_id_existing_address(self):
        address_id = 1
        with patch('address.models.address.Address.objects.get') as mock_get:
            AddressRepository.get_address_by_id(address_id, self.user)
            mock_get.assert_called_once_with(pk=address_id, user=self.user)

    def test_get_address_by_id_non_existing_address(self):
        address_id = 1
        with patch('address.models.address.Address.objects.get') as mock_get:
            mock_get.side_effect = Address.DoesNotExist
            result = AddressRepository.get_address_by_id(address_id, self.user)
            self.assertIsNone(result)

    # def test_update_address_valid_data(self):
    #     address = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')
    #     data = {'city': 'New City'}
    #     with patch('address.serializers.address_serializer.AddressSerializer') as mock_serializer:
    #         mock_serializer.return_value.is_valid.return_value = True
    #         AddressRepository.update_address(address, data)
    #         mock_serializer.assert_called_once_with(address, data=data, partial=True)
    #         mock_serializer.return_value.save.assert_called_once()

    def test_update_address_invalid_data(self):
        address = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')
        data = {'city': ''}
        with patch('address.serializers.address_serializer.AddressSerializer') as mock_serializer:
            mock_serializer.return_value.is_valid.return_value = False
            result = AddressRepository.update_address(address, data)
            self.assertIsInstance(result, dict)  # Expecting errors dictionary

    def test_delete_address(self):
        address = Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345')
        with patch.object(address, 'delete') as mock_delete:
            AddressRepository.delete_address(address)
            mock_delete.assert_called_once()

    # def test_get_user_addresses(self):
    #     addresses = [
    #         Address.objects.create(user=self.user, street_address='123 Main St', city='Anytown', state='ABC', zipcode='12345'),
    #         Address.objects.create(user=self.user, street_address='456 Elm St', city='Othertown', state='XYZ', zipcode='54321')
    #     ]
    #     with patch('address.serializers.address_serializer.AddressSerializer') as mock_serializer:
    #         AddressRepository.get_user_addresses(self.user)
    #         mock_serializer.assert_called_once_with(addresses, many=True)


if __name__ == '__main__':
    unittest.main()
