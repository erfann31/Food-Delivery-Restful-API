from rest_framework import serializers

from restaurant.models import Restaurant
from restaurant.serializers import RestaurantDetailSerializer, RestaurantIdSerializer
from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    restaurant = RestaurantDetailSerializer(read_only=True)  # For GET request
    restaurant_id = RestaurantIdSerializer(write_only=True)  # For POST request

    class Meta:
        model = Food
        fields = '__all__'


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


# Serializer for Food retrieval
class FoodRetrieveSerializer(serializers.ModelSerializer):
    restaurant = RestaurantDetailSerializer()

    class Meta:
        model = Food
        fields = '__all__'
