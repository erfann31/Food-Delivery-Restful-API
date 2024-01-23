from django.contrib import admin

from discount_code.models.discount_code import DiscountCode


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code_text', 'discount_percent', 'is_active']
    search_fields = ['code_text']
    list_filter = ['is_active']

admin.site.register(DiscountCode, DiscountCodeAdmin)
