import random

from restaurant.models.restaurant import Restaurant


class RestaurantRepository:
    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        return Restaurant.objects.get(pk=restaurant_id)

    @staticmethod
    def get_random_restaurants(count):
        return random.sample(list(Restaurant.objects.all()), count)

    @staticmethod
    def generate_random_stars():
        return round(random.uniform(1, 5), 1)

    @staticmethod
    def generate_random_stars_count():
        return random.randint(500, 10000)

    @staticmethod
    def generate_random_distance():
        return round(random.uniform(0.3, 5), 2)
