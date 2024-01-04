from django.urls import path

from . import views

urlpatterns = [
    path('get_restaurant_with_dishes/<int:restaurant_id>/', views.get_restaurant_with_dishes, name='get_restaurant_with_dishes'),
]
