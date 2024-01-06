from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from address.models.address import Address
from discount_code.models.discount_code import DiscountCode
from food.models.food import Food
from order.models.order_item import Order, OrderItem
from order.views import OrderItemViewSet, OrderViewSet
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class CreateOrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.client.force_authenticate(user=self.user)

    @patch('order.serializers.OrderSerializer')
    def test_create_order_success(self, mock_order_serializer):
        mock_serializer_instance = mock_order_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.save.return_value = None

        url = reverse('create_order')
        restaurant = Restaurant.objects.create(name='Test Restaurant')
        address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)

        food1 = Food.objects.create(name='Test Food', price=10.0, stars=4.5, stars_count=500, min_time_to_delivery=20, max_time_to_delivery=40, category='Burger', restaurant=restaurant)
        food2 = Food.objects.create(name='Test Food', price=10.0, stars=4.5, stars_count=500, min_time_to_delivery=20, max_time_to_delivery=40, category='Burger', restaurant=restaurant)

        data = {
            "delivery_address": address.id,
            "orderItems": [
                {"food": food1.id, "quantity": 2},
                {"food": food2.id, "quantity": 3},
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('order.serializers.OrderSerializer')
    def test_create_order_failure(self, mock_order_serializer):
        mock_serializer_instance = mock_order_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'some_field': ['Some error message']}

        url = reverse('create_order')
        data = {
            'delivery_address': 1,
            'orderItems': [
                {'food': 1, 'quantity': 2},
                {'food': 2, 'quantity': 1},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateOrderStatusAPITest(APITestCase):
    @patch('order.views.Order.objects.get')
    def test_update_order_status(self, mock_order_get):
        order_id = 1
        mock_order = mock_order_get.return_value
        mock_order.status = 'Ongoing'

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('update_order_status', kwargs={'order_id': order_id})

        response = self.client.get(url, **headers)

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order status updated to Completed')

    @patch('order.views.Order.objects.get')
    def test_update_order_status_not_found(self, mock_order_get):
        mock_order_get.side_effect = Order.DoesNotExist

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('update_order_status', kwargs={'order_id': 999})  # Non-existing order ID

        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Order not found')


class CancelOrderAPITest(APITestCase):
    @patch('order.views.Order.objects.get')
    def test_cancel_order(self, mock_order_get):
        order_id = 1
        mock_order = mock_order_get.return_value
        mock_order.is_canceled = False

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('cancel_order', kwargs={'order_id': order_id})

        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Order cancelled successfully!')

    @patch('order.views.Order.objects.get')
    def test_cancel_order_not_found(self, mock_order_get):
        mock_order_get.side_effect = Order.DoesNotExist

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('cancel_order', kwargs={'order_id': 999})  # Non-existing order ID

        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Order not found')


class AddDiscountCodeAPITest(APITestCase):
    @patch('order.views.Order.objects.get')
    @patch('order.views.DiscountCode.objects.get')
    def test_add_discount_code_success(self, mock_discount_code_get, mock_order_get):
        order_id = 1
        discount_code_text = 'TESTCODE'

        mock_order = mock_order_get.return_value
        mock_order.total_price = 100
        mock_discount_code = mock_discount_code_get.return_value
        mock_discount_code.discount_percent = 10

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('add_discount_code', kwargs={'order_id': order_id})
        data = {'discount_code': discount_code_text}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], 90)  # Replace with the expected total price after applying the discount

    @patch('order.views.Order.objects.get')
    def test_add_discount_code_invalid_discount_code(self, mock_order_get):
        order_id = 1
        discount_code_text = 'INVALIDCODE'  # Replace with an invalid discount code

        mock_order = mock_order_get.return_value

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('add_discount_code', kwargs={'order_id': order_id})
        data = {'discount_code': discount_code_text}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid or inactive discount code')

    @patch('order.views.Order.objects.get')
    def test_add_discount_code_order_not_found(self, mock_order_get):
        mock_order_get.side_effect = Order.DoesNotExist

        order_id = 1
        discount_code_text = 'TESTCODE'

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('add_discount_code', kwargs={'order_id': order_id})
        data = {'discount_code': discount_code_text}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Order not found')

    # Empty or missing discount code
    @patch('order.views.Order.objects.get')
    def test_add_discount_code_empty_discount_code(self, mock_order_get):
        order_id = 1
        discount_code_text = ''

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('add_discount_code', kwargs={'order_id': order_id})
        data = {'discount_code': discount_code_text}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['discount_code'], 'this field is required!')

    # Inactive or invalid discount code
    @patch('order.views.Order.objects.get')
    @patch('order.views.DiscountCode.objects.get')
    def test_add_discount_code_inactive_or_invalid_discount_code(self, mock_discount_code_get, mock_order_get):
        order_id = 1
        discount_code_text = 'INVALIDCODE'

        mock_order = mock_order_get.return_value

        mock_discount_code_get.side_effect = DiscountCode.DoesNotExist

        user = User.objects.create(email='test@example.com')
        access_token = str(AccessToken.for_user(user))
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        url = reverse('add_discount_code', kwargs={'order_id': order_id})
        data = {'discount_code': discount_code_text}

        response = self.client.post(url, data, **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid or inactive discount code')


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.view = OrderViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)

    def test_list_orders(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        response = self.client.get(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order(self):
        data = {'status': 'Completed'}
        response = self.client.patch(reverse('order-detail', kwargs={'pk': self.order.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        response = self.client.delete(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderItemViewSetTests(APITestCase):
    def setUp(self):
        self.view = OrderItemViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))

    def test_list_order_items(self):
        response = self.client.get(reverse('orderitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order_item(self):
        order_item = OrderItem.objects.create(order=self.order, food=self.food, quantity=2)
        response = self.client.get(reverse('orderitem-detail', kwargs={'pk': order_item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_item(self):
        order_item = OrderItem.objects.create(order=self.order, food=self.food, quantity=2)
        data = {'quantity': 3}
        response = self.client.patch(reverse('orderitem-detail', kwargs={'pk': order_item.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_item(self):
        order_item = OrderItem.objects.create(order=self.order, food=self.food, quantity=2)
        response = self.client.delete(reverse('orderitem-detail', kwargs={'pk': order_item.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
