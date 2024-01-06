from rest_framework import serializers

from restaurant.models.restaurant import Restaurant


# Serializer for POST request
class RestaurantIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id']
