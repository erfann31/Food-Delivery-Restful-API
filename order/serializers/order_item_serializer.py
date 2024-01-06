from rest_framework import serializers

from food.models.food import Food
from order.models.order_item import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']

    def to_representation(self, instance):
        if isinstance(instance, OrderItem):
            return {
                'food_id': instance.food.id,
                'food_name': instance.food.name,
                'price': instance.food.price,
                'category': instance.food.category,
                'quantity': instance.quantity
            }
        return super().to_representation(instance)
