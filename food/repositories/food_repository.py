import random

from consts.constants import CATEGORY_CHOICES
from food.models.food import Food
from food.serializers.food_serializer import FoodSerializer


class FoodRepository:
    @staticmethod
    def get_food_by_id(food_id):
        return Food.objects.get(pk=food_id)
    @staticmethod
    def get_foods_by_category_for_restaurant(restaurant):
        foods_by_category = {}
        for category in CATEGORY_CHOICES:
            foods = Food.objects.filter(restaurant=restaurant, category=category[0]).order_by('category')
            foods_by_category[category[0]] = FoodSerializer(foods, many=True).data
        return foods_by_category

    @staticmethod
    def get_random_foods_by_category(category, count):
        return Food.objects.filter(category=category).order_by('?')[:count]

    @staticmethod
    def get_random_food_categories(count):
        categories = [category[0] for category in CATEGORY_CHOICES]
        return random.sample(categories, count)

    @staticmethod
    def generate_random_stars():
        return round(random.uniform(1, 5), 1)

    @staticmethod
    def generate_random_stars_count():
        return random.randint(5, 1000)

    @staticmethod
    def generate_random_delivery_times():
        min_time = random.randint(15, 75)
        max_time = random.randint(min_time + 15, 90)
        return min_time, max_time