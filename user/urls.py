# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('verify/<str:token>/', views.email_verification_view, name='email-verification'),
    path('delete/', views.delete_user, name='delete'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password-reset-confirm'),

]
