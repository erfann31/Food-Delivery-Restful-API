import unittest
from django.test import TestCase
from user.models import CustomUser
from unittest.mock import patch

from user.serializers.custom_user_serializer import CustomUserSerializer


class CustomUserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_serializer_fields(self):
        serializer = CustomUserSerializer()
        expected_fields = ('id', 'date_joined', 'verified', 'is_active', 'is_staff',
                           'name', 'email', 'photo', 'mobile_number', 'password')
        self.assertEqual(set(serializer.fields.keys()), set(expected_fields))

    def test_password_field_write_only(self):
        serializer = CustomUserSerializer()
        self.assertTrue(serializer.fields['password'].write_only)

    def test_serialization(self):
        serializer = CustomUserSerializer(instance=self.user)
        serialized_data = serializer.data
        self.assertEqual(serialized_data['name'], self.user.name)
        self.assertEqual(serialized_data['email'], self.user.email)

    # def test_create_user(self):
    #     validated_data = {
    #         'name': 'Jane Doe',
    #         'email': 'jane@example.com',
    #         'password': 'password456'
    #     }
    #     with patch.object(CustomUser.objects, 'create_user') as mock_create_user:
    #         serializer = CustomUserSerializer(data=validated_data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         mock_create_user.assert_called_once_with(**validated_data)

if __name__ == '__main__':
    unittest.main()
