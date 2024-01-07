from django.contrib.auth import get_user_model
from django.test import TestCase

from food.models.food import Food
from order.models.order_item import OrderItem
from order.serializers.order_item_serializer import OrderItemSerializer
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class OrderItemSerializerTestCase(TestCase):

    def test_to_representation_method_with_order_item_instance(self):
        food = Food.objects.create(name='Test Food', price=10.0, stars=4.0, stars_count=100, min_time_to_delivery=20, max_time_to_delivery=45, category='Burger', restaurant=Restaurant.objects.create(name='Test Restaurant'))

        order_item = OrderItem(food=food, quantity=2)

        serializer = OrderItemSerializer()
        serialized_data = serializer.to_representation(order_item)

        expected_data = {
            'food_id': food.id,
            'food_name': food.name,
            'price': food.price,
            'category': food.category,
            'quantity': order_item.quantity
        }

        self.assertEqual(serialized_data, expected_data)
