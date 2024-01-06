from rest_framework.viewsets import ModelViewSet

from discount_code.models.discount_code import DiscountCode
from discount_code.serializers import DiscountCodeSerializer


class DiscountCodeViewSet(ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer
