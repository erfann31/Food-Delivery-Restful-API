# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('password_reset/', views.password_reset_request, name='password-reset'),
    path('resend_verification_email/', views.resend_verification_email, name='resend_verification_email'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('get_user_favorites/', views.get_user_favorites, name='get_user_favorites'),
    path('get_information/', views.get_information, name='get_information'),

]
