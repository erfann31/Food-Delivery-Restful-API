from rest_framework import serializers

from user.serializers import CustomUserSerializer
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id',)
