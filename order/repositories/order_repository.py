from order.models.order import Order


class OrderRepository:
    @staticmethod
    def create_order(order_data, user):
        return Order.objects.create(user=user, **order_data)

    @staticmethod
    def get_completed_orders(user):
        return Order.objects.filter(user=user, status='Completed')

    @staticmethod
    def get_ongoing_orders(user):
        return Order.objects.filter(user=user, status='Ongoing')

    def update_order_status(self, user, new_status):
        try:
            order = Order.objects.get(pk=self, user=user)
            order.status = new_status
            order.save()
            return True
        except Order.DoesNotExist:
            return False

    @staticmethod
    def cancel_order(order_id, user):
        try:
            order = Order.objects.get(pk=order_id, user=user)
            order.is_canceled = True
            order.save()
            return True
        except Order.DoesNotExist:
            return False

    @staticmethod
    def get_order_by_id(order_id, user):
        try:
            return Order.objects.get(pk=order_id, user=user)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def apply_discount_code(order, discount_code):
        order.total_price -= (order.total_price * (discount_code.discount_percent / 100))
        order.discount_code = discount_code
        order.save()

    @staticmethod
    def get_user_orders_by_status(user, status):
        return Order.objects.filter(user=user, status=status)

    @staticmethod
    def get_order_by_id_and_user(order_id, user):
        try:
            order = Order.objects.get(pk=order_id, user=user)
            return order
        except Order.DoesNotExist:
            return None
