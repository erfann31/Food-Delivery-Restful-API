from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id',)
