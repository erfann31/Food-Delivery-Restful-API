from django.urls import path

from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('get_user_orders/', views.get_user_orders, name='get_user_orders'),
    path('add_discount_code/<int:order_id>/', views.add_discount_code, name='add_discount_code'),

]
