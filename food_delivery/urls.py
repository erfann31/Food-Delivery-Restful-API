from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from address import views as address_views
from food import views as food_views
from order import views as order_views
from restaurant import views as restaurant
from restaurant import views as restaurant_views
from user import views as user_views

schema_view = get_schema_view(
    openapi.Info(
        title="Food Delivery Services API",
        default_version='v1',
        description="For Food Delivery Services API V1",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="erfannasri2@gmail.com"),
        license=openapi.License(name="@Erfann31"),
    ),
    public=True,
)
router = routers.DefaultRouter()
router.register(r'addresses', address_views.AddressViewSet)
router.register(r'foods', food_views.FoodViewSet)
router.register(r'orders', order_views.OrderViewSet)
router.register(r'order_items', order_views.OrderItemViewSet)
router.register(r'restaurant', restaurant_views.RestaurantViewSet)
router.register(r'users', user_views.CustomUserViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/users/', include('user.urls')),
                  path('api/v1/orders/', include('order.urls')),
                  path('api/v1/addresses/', include('address.urls')),
                  path('api/v1/restaurants/', include('restaurant.urls')),
                  path('api/v1/get_home/', restaurant.get_home, name='get_random_data'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + router.urls
