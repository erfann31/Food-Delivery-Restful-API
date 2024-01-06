from rest_framework import serializers

from food.models.food import Food
from restaurant.serializers import RestaurantDetailSerializer


class FoodRetrieveSerializer(serializers.ModelSerializer):
    restaurant = RestaurantDetailSerializer()

    class Meta:
        model = Food
        fields = '__all__'
