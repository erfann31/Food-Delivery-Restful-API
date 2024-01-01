from rest_framework import serializers

from food.serializers import FoodSerializer
from restaurant.serializers import RestaurantSerializer
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    favorite_restaurants = RestaurantSerializer()
    favorite_foods = FoodSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('id', 'date_joined', 'verified', 'is_active', 'is_staff', 'password_reset_token_created_at', 'password_reset_token', 'verification_token',)
