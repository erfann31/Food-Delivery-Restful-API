from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from discount_code.repositories.discount_code_repository import DiscountCodeRepository
from order.models.order_item import Order
from order.repositories.order_repository import OrderRepository
from order.serializers.order_serializer import OrderSerializer


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

    completed_orders = OrderRepository.get_completed_orders(user)
    ongoing_orders = OrderRepository.get_ongoing_orders(user)

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
    if OrderRepository.update_order_status(order_id, request.user, "Completed"):
        return Response({'message': 'Order status updated to Completed'}, status=status.HTTP_200_OK)
    return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    if OrderRepository.cancel_order(order_id, request.user):
        return Response({'message': 'Order cancelled successfully!'}, status=status.HTTP_200_OK)
    return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_discount_code(request, order_id):
    try:
        order = OrderRepository.get_order_by_id_and_user(order_id, request.user)
        discount_code_text = request.data.get('discount_code')

        if not discount_code_text:
            return Response({'discount_code': 'this field is required!'}, status=status.HTTP_400_BAD_REQUEST)

        discount_code = DiscountCodeRepository.get_discount_code_by_text(discount_code_text)
        if discount_code:
            OrderRepository.apply_discount_code(order, discount_code)
            return Response({'total_price': order.total_price}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid or inactive discount code'}, status=status.HTTP_400_BAD_REQUEST)

    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
