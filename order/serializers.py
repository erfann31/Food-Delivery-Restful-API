from rest_framework import serializers

from address.serializers import AddressSerializer
from food.serializers import FoodSerializer
from user.serializers import CustomUserSerializer
from .models import Order, OrderItem


class OrderItemsSerializer(serializers.ModelSerializer):

    food = FoodSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemsSerializer()
    user = CustomUserSerializer()
    delivery_address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'date_and_time', 'estimated_arrival')
