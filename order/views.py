from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


@api_view(['GET'])
def get_user_orders(request, user_id):
    completed_orders = Order.objects.filter(user=user_id, status='Completed')
    ongoing_orders = Order.objects.filter(user=user_id, status='Ongoing')

    completed_orders_serializer = OrderSerializer(completed_orders, many=True)
    ongoing_orders_serializer = OrderSerializer(ongoing_orders, many=True)

    return Response({
        'completed_orders': completed_orders_serializer.data,
        'ongoing_orders': ongoing_orders_serializer.data
    })


@api_view(['PATCH'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = 'Completed'
        order.save()
        return Response({'message': 'Order status updated to Completed'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_discount_code(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        discount_code = request.data.get('discount_code')
        order.discount_code = discount_code
        order.save()

        return Response({'message': 'Discount code applied to the order'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
