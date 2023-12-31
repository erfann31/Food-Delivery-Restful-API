from rest_framework.response import Response
from rest_framework.decorators import api_view

import food.models as FoodModel
from food.serializers import FoodSerializer
from .models import Restaurant
from .serializers import RestaurantSerializer
import random

@api_view(['GET'])
def get_home(request):
    random_restaurants = random.sample(list(Restaurant.objects.all()), 6)
    restaurant_serializer = RestaurantSerializer(random_restaurants, many=True)

    random_categories = random.sample(FoodModel.CATEGORY_CHOICES, 3)

    food_data = []
    for category in random_categories:
        category_foods = FoodModel.Food.objects.filter(category=category[0]).order_by('?')[:3]
        food_serializer = FoodSerializer(category_foods, many=True)
        food_data.append({
            'category': category[0],
            'foods': food_serializer.data
        })

    return Response({
        'restaurants': restaurant_serializer.data,
        'food_series': food_data
    })




@api_view(['GET'])
def get_restaurant_with_dishes(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        foods_by_category = {}
        for category in dict(FoodModel.CATEGORY_CHOICES).keys():
            foods = FoodModel.Food.objects.filter(restaurant=restaurant, category=category).order_by('category')
            foods_by_category[category] = FoodSerializer(foods, many=True).data

        restaurant_serializer = RestaurantSerializer(restaurant)
        return Response({
            'restaurant': restaurant_serializer.data,
            'dishes_by_category': foods_by_category
        })
    except Restaurant.DoesNotExist:
        return Response({'message': 'Restaurant not found'}, status=404)

