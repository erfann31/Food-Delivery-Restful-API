from rest_framework import serializers

from address.models.address import Address


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id',)
