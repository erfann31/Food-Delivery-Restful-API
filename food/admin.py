from django.contrib import admin

from food.forms.forms import FoodAdminForm
from food.models.food import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    form = FoodAdminForm
    list_display = ['name', 'price', 'stars', 'stars_count', 'min_time_to_delivery', 'max_time_to_delivery', 'category', 'restaurant']
    search_fields = ['name', 'category', 'restaurant']
    list_filter = ['category', 'restaurant']
