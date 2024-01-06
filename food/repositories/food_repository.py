import random

from consts.constants import CATEGORY_CHOICES
from food.models.food import Food
from food.serializers.food_serializer import FoodSerializer


class FoodRepository:
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
