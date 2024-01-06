from rest_framework import serializers

from restaurant.models.restaurant import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('id', 'stars', 'distance', 'stars_count')
