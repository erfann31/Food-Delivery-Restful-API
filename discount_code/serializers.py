from rest_framework import serializers

from discount_code.models.discount_code import DiscountCode


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
        read_only_fields = ('id',)
