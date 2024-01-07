from django.contrib.auth import get_user_model
from django.test import TestCase

from address.models.address import Address
from food.models.food import Food
from order.models.order import Order
from order.models.order_item import OrderItem
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class OrderItemModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.order = Order.objects.create(user=self.user, total_price=50.0, status='Ongoing', delivery_address_id=self.address.id)
        self.food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            food=self.food,
            quantity=2
        )

        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.food, self.food)
        self.assertEqual(order_item.quantity, 2)

    def test_order_item_str_representation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            food=self.food,
            quantity=3
        )

        expected_str = f"{order_item.food.name} - Quantity: {order_item.quantity}"
        self.assertEqual(str(order_item), expected_str)

    def test_order_item_default_quantity(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            food=self.food
        )

        self.assertEqual(order_item.quantity, 1)  # Check if default quantity is set correctly

    def test_order_item_update_quantity(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            food=self.food,
            quantity=2
        )

        order_item.quantity = 5
        order_item.save()

        updated_order_item = OrderItem.objects.get(pk=order_item.pk)
        self.assertEqual(updated_order_item.quantity, 5)  # Check if quantity is updated correctly
