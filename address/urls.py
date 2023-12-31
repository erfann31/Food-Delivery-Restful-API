from django.urls import path
from . import views

urlpatterns = [
    path('create_address/<int:user_id>/', views.create_address, name='create_address'),
    path('edit_or_delete_address/<int:user_id>/<int:address_id>/', views.edit_or_delete_address, name='edit_or_delete_address'),
    path('get_user_addresses/<int:user_id>/', views.get_user_addresses, name='get_user_addresses'),
]

