from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from address.models import Address
from address.views import AddressViewSet
from user.models import CustomUser

User = get_user_model()


class CreateAddressAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.access_token = str(AccessToken.for_user(self.user))

    @patch('address.serializers.AddressSerializer')
    def test_create_address_success(self, mock_address_serializer):
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = None

        url = reverse('create_address')
        data = {'street_address': '123 Test St', 'city': 'Test City', 'state': 'Test State', 'zipcode': '12345'}

        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('address.serializers.AddressSerializer')
    def test_create_address_failure(self, mock_address_serializer):
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'some_field': ['Some error message']}

        url = reverse('create_address')
        data = {'street_address': '123 Test St',
                # 'city': 'Test City',
                'state': 'Test State',
                'zipcode': '12345'}

        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EditOrDeleteAddressAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.access_token = str(AccessToken.for_user(self.user))
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)

    @patch('address.serializers.AddressSerializer')
    def test_edit_address_success(self, mock_address_serializer):
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = None

        url = reverse('edit_or_delete_address', kwargs={'address_id': self.address.id})
        data = {'street_address': '456 Modified St'}

        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.patch(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('address.serializers.AddressSerializer')
    def test_edit_address_failure(self, mock_address_serializer):
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'some_field': ['Some error message']}

        url = reverse('edit_or_delete_address', kwargs={'address_id': self.address.id})
        data = {'street_address': '', 'city': '', 'state': '', 'zipcode': ''}

        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.patch(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_address(self):
        url = reverse('edit_or_delete_address', kwargs={'address_id': self.address.id})

        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.delete(url, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existing_address(self):
        url = reverse('edit_or_delete_address', kwargs={'address_id': 9999})

        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.delete(url, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetUserAddressesAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.access_token = str(AccessToken.for_user(self.user))
        self.address1 = Address.objects.create(user=self.user, street_address='123 Test St', city='Test City 1', state='Test State 1', zipcode='12345')
        self.address2 = Address.objects.create(user=self.user, street_address='456 Test St', city='Test City 2', state='Test State 2', zipcode='67890')

    @patch('address.views.Address.objects.filter')
    @patch('address.serializers.AddressSerializer')
    def test_get_user_addresses(self, mock_address_serializer, mock_address_filter):
        mock_address_filter.return_value = [self.address1, self.address2]

        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.data = [{'street_address': '123 Test St', 'city': 'Test City 1', 'state': 'Test State 1', 'zipcode': '12345'}, {'street_address': '456 Test St', 'city': 'Test City 2', 'state': 'Test State 2', 'zipcode': '67890'}]

        url = reverse('get_user_addresses')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddressViewSetTests(APITestCase):
    def setUp(self):
        self.view = AddressViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'update', 'delete': 'destroy'})
        self.user = CustomUser.objects.create(email='test@example.com', name='Test User')

        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user_id=self.user.id)

    @patch('address.views.Address.objects.filter')
    @patch('address.serializers.AddressSerializer')
    def test_list_addresses(self, mock_address_serializer, mock_address_filter):
        mock_address_filter.return_value = [self.address]
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.data = [{'street_address': '123 Test St', 'city': 'Test City', 'state': 'Test State', 'zipcode': '12345'}]

        url = reverse('address-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('address.views.Address.objects.filter')
    @patch('address.serializers.AddressSerializer')
    def test_retrieve_address(self, mock_address_serializer, mock_address_get):
        mock_address_get.return_value = self.address
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.data = {'street_address': '123 Test St', 'city': 'Test City', 'state': 'Test State', 'zipcode': '12345'}

        url = reverse('address-detail', kwargs={'pk': self.address.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('address.views.Address.objects.filter')
    @patch('address.serializers.AddressSerializer')
    def test_update_address(self, mock_address_serializer, mock_address_get):
        mock_address_get.return_value = self.address
        mock_serializer_instance = mock_address_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = self.address

        url = reverse('address-detail', kwargs={'pk': self.address.pk})
        data = {'street_address': 'Updated St'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('address.views.Address.objects.get')
    def test_delete_address(self, mock_address_get):
        mock_address_get.return_value = self.address

        url = reverse('address-detail', kwargs={'pk': self.address.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
