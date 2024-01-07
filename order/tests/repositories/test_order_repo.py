import unittest
from unittest.mock import Mock, patch

from order.models.order import Order
from order.repositories.order_repository import OrderRepository


class TestOrderRepository(unittest.TestCase):

    @patch('order.models.order.Order.objects')
    def test_create_order(self, mock_order_objects):
        user = Mock()
        order_data = {'total_price': 100, 'status': 'Ongoing'}
        mock_order_objects.create.return_value = Order()

        result = OrderRepository.create_order(order_data, user)
        self.assertIsInstance(result, Order)
        mock_order_objects.create.assert_called_once_with(user=user, **order_data)

    @patch('order.models.order.Order.objects')
    def test_get_completed_orders(self, mock_order_objects):
        user = Mock()
        mock_order_objects.filter.return_value = []

        result = OrderRepository.get_completed_orders(user)
        self.assertEqual(result, [])
        mock_order_objects.filter.assert_called_once_with(user=user, status='Completed')

    @patch('order.models.order.Order.objects')
    def test_update_order_status_existing_order(self, mock_order_objects):
        user = Mock()
        order_instance = Mock()
        mock_order_objects.get.return_value = order_instance

        new_status = 'Completed'
        result = OrderRepository().update_order_status(user, new_status)
        self.assertTrue(result)
        order_instance.save.assert_called_once()

    @patch('order.models.order.Order.objects')
    def test_update_order_status_nonexistent_order(self, mock_order_objects):
        user = Mock()
        mock_order_objects.get.side_effect = Order.DoesNotExist

        new_status = 'Completed'
        result = OrderRepository().update_order_status(user, new_status)
        self.assertFalse(result)

    @patch('order.models.order.Order.objects')
    def test_cancel_order_existing_order(self, mock_order_objects):
        order_id = 1
        user = Mock()
        order_instance = Mock()
        mock_order_objects.get.return_value = order_instance

        result = OrderRepository.cancel_order(order_id, user)
        self.assertTrue(result)
        order_instance.save.assert_called_once_with()

    @patch('order.models.order.Order.objects')
    def test_get_order_by_id_existing_order(self, mock_order_objects):
        order_id = 1
        user = Mock()
        order_instance = Mock()
        mock_order_objects.get.return_value = order_instance

        result = OrderRepository().get_order_by_id(order_id, user)
        self.assertEqual(result, order_instance)
        mock_order_objects.get.assert_called_once_with(pk=order_id, user=user)

    @patch('order.models.order.Order.objects')
    def test_get_order_by_id_nonexistent_order(self, mock_order_objects):
        order_id = 1
        user = Mock()
        mock_order_objects.get.side_effect = Order.DoesNotExist

        result = OrderRepository().get_order_by_id(order_id, user)
        self.assertIsNone(result)

    @patch('order.models.order.Order.objects')
    def test_apply_discount_code(self, mock_order_objects):
        order_instance = Mock()
        discount_code = Mock()
        discount_code.discount_percent = 10
        order_instance.total_price = 100
        mock_order_objects.get.return_value = order_instance

        OrderRepository.apply_discount_code(order_instance, discount_code)
        order_instance.save.assert_called_once()
        self.assertEqual(order_instance.total_price, 90)
        self.assertEqual(order_instance.discount_code, discount_code)

    @patch('order.models.order.Order.objects')
    def test_get_user_orders_by_status(self, mock_order_objects):
        user = Mock()
        status = 'Completed'
        mock_order_objects.filter.return_value = []

        result = OrderRepository().get_user_orders_by_status(user, status)
        self.assertEqual(result, [])
        mock_order_objects.filter.assert_called_once_with(user=user, status=status)


if __name__ == '__main__':
    unittest.main()
