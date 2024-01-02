from django.urls import path

from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('get_user_orders/', views.get_user_orders, name='get_user_orders'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('add_discount_code/<int:order_id>/', views.add_discount_code, name='add_discount_code'),

]
