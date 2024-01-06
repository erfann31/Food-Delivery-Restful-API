import random

from restaurant.models.restaurant import Restaurant


class RestaurantRepository:
    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        return Restaurant.objects.get(pk=restaurant_id)

    @staticmethod
    def get_random_restaurants(count):
        return random.sample(list(Restaurant.objects.all()), count)
