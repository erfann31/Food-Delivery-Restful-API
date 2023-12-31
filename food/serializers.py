from rest_framework import serializers

from restaurant.serializers import RestaurantSerializer
from .models import Food


class FoodSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Food
        fields = '__all__'
        read_only_fields = ('id', 'stars_count', 'stars')
