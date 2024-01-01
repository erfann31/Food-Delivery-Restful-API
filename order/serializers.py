from rest_framework import serializers

from address.models import Address
from address.serializers import AddressSerializer
from food.models import Food
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    delivery_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    orderItems = OrderItemSerializer(many=True, required=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'date_and_time', 'delivery_address', 'discount_code', 'estimated_arrival', 'is_canceled', 'orderItems']
        read_only_fields = ['id', 'date_and_time', 'orderItems', 'estimated_arrival']

    def create(self, validated_data):
        order_items_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['delivery_address'] = AddressSerializer(instance.delivery_address).data
        representation['orderItems'] = OrderItemSerializer(instance.orderitem_set.all(), many=True).data
        representation['discount_code'] = instance.discount_code if instance.discount_code else None
        return representation
