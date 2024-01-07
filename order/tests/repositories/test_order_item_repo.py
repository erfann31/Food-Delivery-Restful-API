import unittest
from unittest.mock import Mock, patch

from order.models.order_item import OrderItem
from order.repositories.order_item_repository import OrderItemRepository


class TestOrderItemRepository(unittest.TestCase):

    @patch('order.models.order_item.OrderItem.objects')
    def test_create_order_item(self, mock_order_item_objects):
        # Mocking necessary parts for create_order_item method
        order_item_data = {'order': Mock(), 'food': Mock(), 'quantity': 2}
        mock_order_item_objects.create.return_value = OrderItem()

        # Testing create_order_item method
        result = OrderItemRepository.create_order_item(order_item_data)
        self.assertIsInstance(result, OrderItem)
        mock_order_item_objects.create.assert_called_once_with(**order_item_data)

    @patch('order.models.order_item.OrderItem.objects')
    def test_get_order_items(self, mock_order_item_objects):
        # Mocking necessary parts for get_order_items method
        order = Mock()
        mock_order_item_objects.filter.return_value = []

        # Testing get_order_items method
        result = OrderItemRepository.get_order_items(order)
        self.assertEqual(result, [])
        mock_order_item_objects.filter.assert_called_once_with(order=order)

    @patch('order.models.order_item.OrderItem.objects')
    def test_get_order_item_by_id_existing(self, mock_order_item_objects):
        # Mocking necessary parts for get_order_item_by_id method when order item exists
        order_item_id = 1
        mock_order_item_objects.get.return_value = OrderItem()

        # Testing get_order_item_by_id method for an existing order item
        result = OrderItemRepository.get_order_item_by_id(order_item_id)
        self.assertIsInstance(result, OrderItem)
        mock_order_item_objects.get.assert_called_once_with(id=order_item_id)

    @patch('order.models.order_item.OrderItem.objects')
    def test_get_order_item_by_id_nonexistent(self, mock_order_item_objects):
        # Mocking necessary parts for get_order_item_by_id method when order item does not exist
        order_item_id = 1
        mock_order_item_objects.get.side_effect = OrderItem.DoesNotExist

        # Testing get_order_item_by_id method for a non-existent order item
        result = OrderItemRepository.get_order_item_by_id(order_item_id)
        self.assertIsNone(result)

    @patch('order.models.order_item.OrderItem.objects')
    def test_update_order_item_existing(self, mock_order_item_objects):
        # Mocking necessary parts for update_order_item method when order item exists
        order_item_id = 1
        new_data = {'quantity': 3}
        order_item_instance = Mock()
        mock_order_item_objects.get.return_value = order_item_instance

        # Testing update_order_item method for an existing order item
        result = OrderItemRepository.update_order_item(order_item_id, new_data)
        self.assertTrue(result)
        order_item_instance.save.assert_called_once()

    @patch('order.models.order_item.OrderItem.objects')
    def test_update_order_item_nonexistent(self, mock_order_item_objects):
        # Mocking necessary parts for update_order_item method when order item does not exist
        order_item_id = 1
        new_data = {'quantity': 3}
        mock_order_item_objects.get.side_effect = OrderItem.DoesNotExist

        # Testing update_order_item method for a non-existent order item
        result = OrderItemRepository.update_order_item(order_item_id, new_data)
        self.assertFalse(result)

    @patch('order.models.order_item.OrderItem.objects')
    def test_delete_order_item_existing(self, mock_order_item_objects):
        # Mocking necessary parts for delete_order_item method when order item exists
        order_item_id = 1
        order_item_instance = Mock()
        mock_order_item_objects.get.return_value = order_item_instance

        # Testing delete_order_item method for an existing order item
        result = OrderItemRepository.delete_order_item(order_item_id)
        self.assertTrue(result)
        order_item_instance.delete.assert_called_once()

    @patch('order.models.order_item.OrderItem.objects')
    def test_delete_order_item_nonexistent(self, mock_order_item_objects):
        # Mocking necessary parts for delete_order_item method when order item does not exist
        order_item_id = 1
        mock_order_item_objects.get.side_effect = OrderItem.DoesNotExist

        # Testing delete_order_item method for a non-existent order item
        result = OrderItemRepository.delete_order_item(order_item_id)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
