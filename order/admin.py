from django.contrib import admin

from order.models.order import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'is_canceled', 'date_and_time', 'delivery_address', 'discount_code', 'estimated_arrival', ]
    list_filter = ['status', 'is_canceled']
    search_fields = ['user__email', 'id']
    actions = ['cancel_orders', 'mark_as_delivered']
    readonly_fields = ['id', 'user', 'total_price', 'date_and_time', 'delivery_address', 'discount_code', 'estimated_arrival', ]

    def cancel_orders(self, request, queryset):
        queryset.update(status='Completed', is_canceled=True)

    cancel_orders.short_description = "Cancel selected orders"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Completed', is_canceled=False)

    mark_as_delivered.short_description = "Completed selected orders"


admin.site.register(Order, OrderAdmin)
