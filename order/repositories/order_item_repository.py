from order.models.order_item import OrderItem

class OrderItemRepository:
    @staticmethod
    def create_order_item(order_item_data):
        return OrderItem.objects.create(**order_item_data)

    @staticmethod
    def get_order_items(order):
        return OrderItem.objects.filter(order=order)

    @staticmethod
    def get_order_item_by_id(order_item_id):
        try:
            return OrderItem.objects.get(id=order_item_id)
        except OrderItem.DoesNotExist:
            return None

    @staticmethod
    def update_order_item(order_item_id, new_data):
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            for attr, value in new_data.items():
                setattr(order_item, attr, value)
            order_item.save()
            return True
        except OrderItem.DoesNotExist:
            return False

    @staticmethod
    def delete_order_item(order_item_id):
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.delete()
            return True
        except OrderItem.DoesNotExist:
            return False