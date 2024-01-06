from rest_framework import serializers

from food.models.food import Food
from restaurant.serializers.restaurant_detail_serializer import RestaurantDetailSerializer
from restaurant.serializers.restaurant_id_serializer import RestaurantIdSerializer


class FoodSerializer(serializers.ModelSerializer):
    restaurant = RestaurantDetailSerializer(read_only=True)  # For GET request
    restaurant_id = RestaurantIdSerializer(write_only=True)  # For POST request

    class Meta:
        model = Food
        fields = '__all__'
