from rest_framework.viewsets import ModelViewSet

from food.models import Food
from food.serializers import FoodSerializer


class FoodViewSet(ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
