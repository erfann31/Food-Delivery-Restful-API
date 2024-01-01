from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.authtoken import views

from address import views as address_views
from discount_code import views as discount_code_views
from food import views as food_views
from order import views as order_views
from restaurant import views as restaurant
from restaurant import views as restaurant_views
from user import views as user_views
from user.views import TokenObtainPairView

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
router.register(r'discount_codes', discount_code_views.DiscountCodeViewSet)

urlpatterns = [
                  path('api-token-auth/', views.obtain_auth_token),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('admin/', admin.site.urls),
                  path('api/v1/users/', include('user.urls')),
                  path('api/v1/orders/', include('order.urls')),
                  path('api/v1/addresses/', include('address.urls')),
                  path('api/v1/restaurants/', include('restaurant.urls')),
                  path('api/v1/get_home/', restaurant.get_home, name='get_random_data'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
