import random

from consts.constants import CATEGORY_CHOICES
from food.models.food import Food
from food.serializers.food_serializer import FoodSerializer
from food.utils.save_food_utility import generate_random_stars, generate_random_stars_count, generate_random_delivery_times
from food.utils.validate_time_range import validate_time_range


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
    def save_food_with_random_attrs(name, price, category, restaurant):
        stars = generate_random_stars()
        stars_count = generate_random_stars_count()
        min_time_to_delivery, max_time_to_delivery = generate_random_delivery_times()

        validate_time_range(min_time_to_delivery, max_time_to_delivery)

        food = Food(
            name=name,
            price=price,
            stars=stars,
            stars_count=stars_count,
            min_time_to_delivery=min_time_to_delivery,
            max_time_to_delivery=max_time_to_delivery,
            category=category,
            restaurant=restaurant,
        )
        food.save()
        return food