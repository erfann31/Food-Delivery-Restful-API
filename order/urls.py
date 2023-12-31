from django.urls import path
from . import views

urlpatterns = [
    path('get_user_orders/<int:user_id>/', views.get_user_orders, name='get_user_orders'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('add_discount_code/<int:order_id>/', views.add_discount_code, name='add_discount_code'),

]
