import unittest
from unittest.mock import Mock, patch

from order.models.order import Order
from order.repositories.order_repository import OrderRepository


class TestOrderRepository(unittest.TestCase):

    @patch('order.models.order.Order.objects')
    def test_create_order(self, mock_order_objects):
        # Mocking necessary parts for create_order method
        user = Mock()
        order_data = {'total_price': 100, 'status': 'Ongoing'}
        mock_order_objects.create.return_value = Order()

        # Testing create_order method
        result = OrderRepository.create_order(order_data, user)
        self.assertIsInstance(result, Order)
        mock_order_objects.create.assert_called_once_with(user=user, **order_data)

    @patch('order.models.order.Order.objects')
    def test_get_completed_orders(self, mock_order_objects):
        # Mocking necessary parts for get_completed_orders method
        user = Mock()
        mock_order_objects.filter.return_value = []

        # Testing get_completed_orders method
        result = OrderRepository.get_completed_orders(user)
        self.assertEqual(result, [])
        mock_order_objects.filter.assert_called_once_with(user=user, status='Completed')

    @patch('order.models.order.Order.objects')
    def test_update_order_status_existing_order(self, mock_order_objects):
        # Mocking necessary parts for update_order_status method
        user = Mock()
        order_instance = Mock()
        mock_order_objects.get.return_value = order_instance

        # Testing update_order_status method for an existing order
        new_status = 'Completed'
        result = OrderRepository().update_order_status(user, new_status)
        self.assertTrue(result)
        order_instance.save.assert_called_once()

    @patch('order.models.order.Order.objects')
    def test_update_order_status_nonexistent_order(self, mock_order_objects):
        # Mocking necessary parts for update_order_status method when order does not exist
        user = Mock()
        mock_order_objects.get.side_effect = Order.DoesNotExist

        # Testing update_order_status method for a non-existent order
        new_status = 'Completed'
        result = OrderRepository().update_order_status(user, new_status)
        self.assertFalse(result)

    @patch('order.models.order.Order.objects')
    def test_cancel_order_existing_order(self, mock_order_objects):
        # Mocking necessary parts for cancel_order method
        order_id = 1
        user = Mock()
        order_instance = Mock()
        mock_order_objects.get.return_value = order_instance

        # Testing cancel_order method for an existing order
        result = OrderRepository.cancel_order(order_id, user)
        self.assertTrue(result)
        order_instance.save.assert_called_once_with()

    @patch('order.models.order.Order.objects')
    def test_get_order_by_id_existing_order(self, mock_order_objects):
        # Mocking necessary parts for get_order_by_id method when order exists
        order_id = 1
        user = Mock()
        order_instance = Mock()
        mock_order_objects.get.return_value = order_instance

        # Testing get_order_by_id method for an existing order
        result = OrderRepository().get_order_by_id(order_id, user)
        self.assertEqual(result, order_instance)
        mock_order_objects.get.assert_called_once_with(pk=order_id, user=user)

    @patch('order.models.order.Order.objects')
    def test_get_order_by_id_nonexistent_order(self, mock_order_objects):
        # Mocking necessary parts for get_order_by_id method when order does not exist
        order_id = 1
        user = Mock()
        mock_order_objects.get.side_effect = Order.DoesNotExist

        # Testing get_order_by_id method for a non-existent order
        result = OrderRepository().get_order_by_id(order_id, user)
        self.assertIsNone(result)

    @patch('order.models.order.Order.objects')
    def test_apply_discount_code(self, mock_order_objects):
        # Mocking necessary parts for apply_discount_code method
        order_instance = Mock()
        discount_code = Mock()
        discount_code.discount_percent = 10
        order_instance.total_price = 100
        mock_order_objects.get.return_value = order_instance

        # Testing apply_discount_code method
        OrderRepository.apply_discount_code(order_instance, discount_code)
        order_instance.save.assert_called_once()
        self.assertEqual(order_instance.total_price, 90)
        self.assertEqual(order_instance.discount_code, discount_code)

    @patch('order.models.order.Order.objects')
    def test_get_user_orders_by_status(self, mock_order_objects):
        # Mocking necessary parts for get_user_orders_by_status method
        user = Mock()
        status = 'Completed'
        mock_order_objects.filter.return_value = []

        # Testing get_user_orders_by_status method
        result = OrderRepository().get_user_orders_by_status(user, status)
        self.assertEqual(result, [])
        mock_order_objects.filter.assert_called_once_with(user=user, status=status)


if __name__ == '__main__':
    unittest.main()
