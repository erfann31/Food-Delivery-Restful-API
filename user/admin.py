from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['email', 'name', 'is_active', 'is_staff', 'date_joined', 'verified']
    search_fields = ['email', 'name']
    readonly_fields = ['verified', 'email', 'favorite_restaurants', 'favorite_foods', 'name', 'mobile_number', 'date_joined', 'password_reset_token_created_at', 'last_login']
    list_filter = ['verified', 'is_staff', 'is_superuser', 'is_active']

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal Info'), {'fields': ('name', 'mobile_number', 'favorite_restaurants', 'favorite_foods')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'verified', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )

    ordering = ['email']

    def get_readonly_fields(self, request, obj=None):
        # Make specified fields read-only for all users
        if obj:
            return self.readonly_fields + [ 'mobile_number', 'favorite_restaurants', 'favorite_foods']
        return self.readonly_fields


admin.site.register(CustomUser, CustomUserAdmin)
