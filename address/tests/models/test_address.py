import unittest

from django.test import TestCase

from address.models.address import Address
from user.models import CustomUser


class AddressModelTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create(name='testuser', email='test@example.com')

    def test_address_str_method(self):
        # Test the __str__ method of Address model
        address = Address.objects.create(
            street_address='123 Main St',
            city='Anytown',
            state='ABC',
            zipcode='12345',
            user=self.user
        )
        expected_output = "123 Main St, Anytown, ABC - 12345"
        self.assertEqual(str(address), expected_output)

    def test_address_user_relationship(self):
        # Create an Address object using the test user created in setUp
        address = Address.objects.create(
            street_address='456 Elm St',
            city='Othertown',
            state='XYZ',
            zipcode='54321',
            user=self.user
        )
        # Assert that the Address user is the same instance as the test user
        self.assertEqual(address.user, self.user)

    def test_address_creation(self):
        # Test creating an Address object
        address = Address.objects.create(
            street_address='789 Oak St',
            city='Sometown',
            state='DEF',
            zipcode='67890',
            user=self.user
        )
        self.assertIsInstance(address, Address)
        self.assertEqual(address.street_address, '789 Oak St')
        self.assertEqual(address.city, 'Sometown')
        self.assertEqual(address.state, 'DEF')
        self.assertEqual(address.zipcode, '67890')
        self.assertEqual(address.user, self.user)


if __name__ == '__main__':
    unittest.main()
