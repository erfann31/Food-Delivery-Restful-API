from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from discount_code.models import DiscountCode
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemsSerializer


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
        discount_code_text = request.data.get('discount_code')
        try:
            discount_code = DiscountCode.objects.get(code_text=discount_code_text, is_active=True)
            order.total_price -= (order.total_price * (discount_code.discount_percent / 100))
            order.discount_code = discount_code
            order.save()
            return Response({'message': 'Discount code applied to the order'}, status=status.HTTP_200_OK)
        except DiscountCode.DoesNotExist:
            return Response({'message': 'Invalid or inactive discount code'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemsSerializer
