import random

from consts.constants import ESTIMATED_ARRIVAL_CHOICES
from order.models.order import Order


class OrderRepository:
    @staticmethod
    def create_order(order_data, user):
        return Order.objects.create(user=user, **order_data)

    @staticmethod
    def generate_random_estimated_arrival():
        return random.choice([i for i, _ in ESTIMATED_ARRIVAL_CHOICES])
    @staticmethod
    def get_completed_orders(user):
        return Order.objects.filter(user=user, status='Completed')

    @staticmethod
    def get_ongoing_orders(user):
        return Order.objects.filter(user=user, status='Ongoing')

    def update_order_status(order_id, user, new_status):
        try:
            order = Order.objects.get(pk=order_id, user=user)
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

    def get_user_orders_by_status(user, status):
        return Order.objects.filter(user=user, status=status)
