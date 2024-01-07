from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from address.models.address import Address
from address.serializers.address_serializer import AddressSerializer
from food.models.food import Food
from order.models.order import Order
from order.models.order_item import OrderItem
from order.serializers.order_serializer import OrderSerializer
from restaurant.models.restaurant import Restaurant

User = get_user_model()


# class OrderSerializerCreateTestCase(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(email='test@example.com')
#         self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
#         self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
#         self.food1 = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))
#         self.food2 = Food.objects.create(name='Test Food', price=20.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))
#
#     @patch('order.models.order.Order.objects.create')
#     @patch('order.models.order_item.OrderItem.objects.create')
#     def test_create_order_with_items(self, mock_order_item_create, mock_order_create):
#         # Mocked instances for testing
#         mock_order_item_create.side_effect = lambda **kwargs: OrderItem(**kwargs)
#         mock_order_create.side_effect = lambda **kwargs: Order(**kwargs)
#
#         data = {
#             'delivery_address': self.address.id,  # Replace with valid address ID
#             'orderItems': [
#                 {'food': self.food1.id, 'quantity': 2},  # Replace with valid food ID
#                 {'food': self.food2.id, 'quantity': 3}  # Replace with valid food ID
#             ],
#         }
#
#         serializer = OrderSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#
#         created_order = serializer.save()
#
#         # Assertions for the mocked create methods
#         mock_order_create.assert_called_once()
#         mock_order_item_create.assert_any_call(order=created_order, food=1, quantity=2)
#         mock_order_item_create.assert_any_call(order=created_order, food=2, quantity=3)
#

class OrderSerializerToRepresentationMethodTestCase(TestCase):

    def test_to_representation_method(self):
        user = User.objects.create(email='test@example.com')
        address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=user)
        order = Order.objects.create(user=user, total_price=50.11, status='Ongoing', delivery_address_id=address.id)
        serializer = OrderSerializer()

        representation = serializer.to_representation(order)

        self.assertEqual(representation['id'], 1)
        self.assertEqual(representation['total_price'], "50.11")
        self.assertEqual(representation['status'], 'Ongoing')
        self.assertEqual(representation['delivery_address'], AddressSerializer(instance=address).data)
        self.assertIsNotNone(representation['orderItems'])
        # Add more assertions as needed
