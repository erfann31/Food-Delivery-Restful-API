from django.contrib import admin

from restaurant.models.restaurant import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'stars', 'stars_count', 'distance', 'address', 'courier_price', 'opening_time']
    search_fields = ['name', 'address']
    list_filter = ['category']


admin.site.register(Restaurant, RestaurantAdmin)
