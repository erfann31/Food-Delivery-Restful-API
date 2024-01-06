from rest_framework import serializers

from food.models.food import Food
from restaurant.models.restaurant import Restaurant


class FoodCreateSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True,
        source='restaurant'
    )

    class Meta:
        model = Food
        fields = [
            'restaurant_id',
            'name',
            'price',
            'min_time_to_delivery',
            'max_time_to_delivery',
            'category',
        ]
