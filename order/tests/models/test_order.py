from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from address.models.address import Address
from consts.constants import ONGOING
from order.models.order import Order
from order.utils.save_order_utility import generate_random_estimated_arrival
from restaurant.models.restaurant import Restaurant

User = get_user_model()


class OrderModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.address = Address.objects.create(street_address='123 Test St', city='Test City', state='Test State', zipcode='12345', user=self.user)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=50.00,
            status=ONGOING,
            delivery_address=self.address,
            estimated_arrival=30,
            is_canceled=False
        )

        self.assertEqual(order.total_price, 50.00)
        self.assertEqual(order.status, ONGOING)
        self.assertEqual(order.delivery_address, self.address)
        lower_bound = 20.0
        upper_bound = 90.0

        self.assertGreaterEqual(order.estimated_arrival, lower_bound)
        self.assertLessEqual(order.estimated_arrival, upper_bound)
        self.assertEqual(order.is_canceled, False)

    @patch('order.utils.save_order_utility.generate_random_estimated_arrival')
    def test_generate_random_estimated_arrival(self, mock_estimated_arrival):
        mock_estimated_arrival.return_value = 45
        estimated_arrival = generate_random_estimated_arrival()
        lower_bound = 20.0
        upper_bound = 90.0

        self.assertGreaterEqual(estimated_arrival, lower_bound)
        self.assertLessEqual(estimated_arrival, upper_bound)

    def test_order_save(self):
        with patch('order.utils.save_order_utility.generate_random_estimated_arrival') as mock_estimated_arrival:
            mock_estimated_arrival.return_value = 60
            order = Order.objects.create(
                user=self.user,
                total_price=50.00,
                status=ONGOING,
                delivery_address=self.address,
                is_canceled=False
            )
            order.save()
            lower_bound = 20.0
            upper_bound = 90.0

            self.assertGreaterEqual(order.estimated_arrival, lower_bound)
            self.assertLessEqual(order.estimated_arrival, upper_bound)
