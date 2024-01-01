from rest_framework import serializers

from user.serializers import CustomUserSerializer
from .models import DiscountCode


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
        read_only_fields = ('id',)
