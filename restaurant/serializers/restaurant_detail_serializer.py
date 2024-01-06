from rest_framework import serializers

from restaurant.models.restaurant import Restaurant

# Serializer for GET request
class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

