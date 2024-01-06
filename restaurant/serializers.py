from rest_framework import serializers

from restaurant.models.restaurant import Restaurant


class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


# Serializer for POST request
class RestaurantIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id']


# Serializer for GET request
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('id', 'stars', 'distance', 'stars_count')
