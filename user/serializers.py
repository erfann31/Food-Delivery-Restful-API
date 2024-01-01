from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'date_joined', 'verified', 'is_active', 'is_staff', 'name', 'email', 'photo', 'mobile_number', 'password')
        read_only_fields = ('id', 'date_joined', 'verified', 'is_active', 'is_staff',)
