from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authtoken import views

from restaurant import views as restaurant
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


urlpatterns = [
                  path('verify/<str:token>/', user_views.email_verification_view, name='email-verification'),
                  path('password-reset/<str:token>/', user_views.password_reset_confirm, name='password-reset-confirm'),
                  path('api-token-auth/', views.obtain_auth_token),
                  path('api/token/', user_views.login_view, name='token_obtain_pair'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('admin/', admin.site.urls),
                  path('api/v1/users/', include('user.urls')),
                  path('api/v1/orders/', include('order.urls')),
                  path('api/v1/addresses/', include('address.urls')),
                  path('api/v1/restaurants/', include('restaurant.urls')),
                  path('api/v1/get_home/', restaurant.get_home, name='get_random_data'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
