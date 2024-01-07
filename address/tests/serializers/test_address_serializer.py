from django.test import TestCase
from rest_framework import serializers

from address.models.address import Address
from address.serializers.address_serializer import AddressSerializer


class TestAddressSerializer(TestCase):

    def test_address_serializer_user_read_only(self):
        serializer = AddressSerializer()
        self.assertTrue(serializer.fields['user'].read_only)

    def test_address_serializer_user_default_value(self):
        serializer = AddressSerializer()
        self.assertIsInstance(serializer.fields['user'].default, serializers.CurrentUserDefault)

    def test_address_serializer_model_and_fields(self):
        serializer = AddressSerializer()

        self.assertEqual(serializer.Meta.model, Address)
        self.assertEqual(serializer.Meta.fields, '__all__')

    def test_address_serializer_read_only_fields(self):
        serializer = AddressSerializer()

        self.assertIn('id', serializer.Meta.read_only_fields)
        self.assertEqual(len(serializer.Meta.read_only_fields), 1)
