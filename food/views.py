from rest_framework.viewsets import ModelViewSet

from food.models.food import Food
from food.serializers.food_create_serializer import FoodCreateSerializer
from food.serializers.food_retrieve_serializer import FoodRetrieveSerializer
from food.serializers.food_serializer import FoodSerializer


class FoodViewSet(ModelViewSet):
    queryset = Food.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return FoodCreateSerializer
        elif self.action == 'retrieve':
            return FoodRetrieveSerializer
        return FoodSerializer
