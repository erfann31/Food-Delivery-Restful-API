# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('verify/<str:token>/', views.email_verification_view, name='email-verification'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('get_user_favorites/', views.get_user_favorites, name='get_user_favorites'),

]
