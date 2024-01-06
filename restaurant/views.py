from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from food.repositories.food_repository import FoodRepository
from food.serializers.food_serializer import FoodSerializer
from restaurant.models.restaurant import Restaurant
from restaurant.repositories.restaurant_repository import RestaurantRepository
from restaurant.serializers.restaurant_serializer import RestaurantSerializer


@api_view(['GET'])
def get_home(request):
    random_restaurants = RestaurantRepository.get_random_restaurants(6)
    restaurant_serializer = RestaurantSerializer(random_restaurants, many=True)

    random_categories = FoodRepository.get_random_food_categories(3)

    food_data = []
    for category in random_categories:
        category_foods = FoodRepository.get_random_foods_by_category(category, 3)
        food_serializer = FoodSerializer(category_foods, many=True)
        food_data.append({
            'category': category,
            'foods': food_serializer.data
        })

    return Response({
        'restaurants': restaurant_serializer.data,
        'food_series': food_data
    })


@api_view(['GET'])
def get_restaurant_with_dishes(request, restaurant_id):
    try:
        restaurant = RestaurantRepository.get_restaurant_by_id(restaurant_id)
        foods_by_category = FoodRepository.get_foods_by_category_for_restaurant(restaurant)

        restaurant_serializer = RestaurantSerializer(restaurant)
        return Response({
            'restaurant': restaurant_serializer.data,
            'dishes_by_category': foods_by_category
        })
    except Restaurant.DoesNotExist:
        return Response({'message': 'Restaurant not found'}, status=404)

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer