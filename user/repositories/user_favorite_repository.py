from user.models import CustomUser

class UserFavoriteRepository:
    @staticmethod
    def add_favorite_restaurant(user_id, restaurant_id):
        user = CustomUser.objects.filter(pk=user_id).first()
        if user:
            user.favorite_restaurants.add(restaurant_id)

    @staticmethod
    def remove_favorite_restaurant(user_id, restaurant_id):
        user = CustomUser.objects.filter(pk=user_id).first()
        if user:
            user.favorite_restaurants.remove(restaurant_id)

    @staticmethod
    def add_favorite_food(user_id, food_id):
        user = CustomUser.objects.filter(pk=user_id).first()
        if user:
            user.favorite_foods.add(food_id)

    @staticmethod
    def remove_favorite_food(user_id, food_id):
        user = CustomUser.objects.filter(pk=user_id).first()
        if user:
            user.favorite_foods.remove(food_id)

    @staticmethod
    def get_user_favorites(user_id):
        try:
            custom_user = CustomUser.objects.get(pk=user_id)
            favorite_restaurants = custom_user.favorite_restaurants.all()
            favorite_foods = custom_user.favorite_foods.all()
            return favorite_restaurants, favorite_foods
        except CustomUser.DoesNotExist:
            return None, None