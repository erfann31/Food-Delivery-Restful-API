from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from discount_code.models.discount_code import DiscountCode
from order.models.order_item import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    user = request.user

    completed_orders = Order.objects.filter(user=user, status='Completed')
    ongoing_orders = Order.objects.filter(user=user, status='Ongoing')

    completed_orders_serializer = OrderSerializer(completed_orders, many=True)
    ongoing_orders_serializer = OrderSerializer(ongoing_orders, many=True)

    return Response({
        'completed_orders': completed_orders_serializer.data,
        'ongoing_orders': ongoing_orders_serializer.data
    })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
        order.status = 'Completed'
        order.save()
        return Response({'message': 'Order status updated to Completed'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
        order.is_canceled = True
        order.save()
        return Response({'message': 'Order cancelled successfully!'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_discount_code(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
        discount_code_text = request.data.get('discount_code')

        if not discount_code_text:
            return Response({'discount_code': 'this field is required!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            discount_code = DiscountCode.objects.get(code_text=discount_code_text, is_active=True)
            order.total_price -= (order.total_price * (discount_code.discount_percent / 100))
            order.discount_code = discount_code
            order.save()
            return Response({'total_price': order.total_price}, status=status.HTTP_200_OK)
        except DiscountCode.DoesNotExist:
            return Response({'message': 'Invalid or inactive discount code'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
