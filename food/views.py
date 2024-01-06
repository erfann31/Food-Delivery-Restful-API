from rest_framework.viewsets import ModelViewSet

from food.models.food import Food
from food.serializers import FoodSerializer, FoodCreateSerializer, FoodRetrieveSerializer


class FoodViewSet(ModelViewSet):
    queryset = Food.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return FoodCreateSerializer
        elif self.action == 'retrieve':
            return FoodRetrieveSerializer
        return FoodSerializer
