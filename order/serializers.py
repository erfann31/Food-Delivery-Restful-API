from rest_framework import serializers

from address.models import Address
from address.serializers import AddressSerializer
from discount_code.models import DiscountCode
from discount_code.serializers import DiscountCodeSerializer
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
    discount_code = serializers.PrimaryKeyRelatedField(queryset=DiscountCode.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'discount_code', 'status', 'date_and_time', 'delivery_address', 'estimated_arrival', 'is_canceled', 'orderItems']
        read_only_fields = ['id', 'date_and_time', 'orderItems', 'estimated_arrival', 'total_price']

    def create(self, validated_data):
        discount_code = validated_data.pop('discount_code', None)
        order_items_data = validated_data.pop('orderitem_set')

        order = Order.objects.create(**validated_data)

        total_price = 0

        for order_item_data in order_items_data:
            food = order_item_data['food']
            quantity = order_item_data['quantity']
            food_price = food.price * quantity
            total_price += food_price  # Accumulate total price

            OrderItem.objects.create(order=order, **order_item_data)

        order.total_price = total_price  # Assign the total price to the order instance
        order.save(update_fields=['total_price'])  # Save the order with the calculated total_price

        if discount_code:
            order.discount_code = discount_code
            order.save(update_fields=['discount_code'])

        return order
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['delivery_address'] = AddressSerializer(instance.delivery_address).data
        representation['orderItems'] = OrderItemSerializer(instance.orderitem_set.all(), many=True).data
        representation['discount_code'] = DiscountCodeSerializer(instance.discount_code).data if instance.discount_code else None
        return representation