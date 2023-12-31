
from django.contrib import admin
from django.urls import include, path

from restaurant import views as restaurant

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),
    path('orders/', include('order.urls')),
    path('addresses/', include('address.urls')),
    path('restaurants/', include('restaurant.urls')),
    path('get_home/', restaurant.get_home, name='get_random_data'),
]
