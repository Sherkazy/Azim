
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path

from rest_framework_simplejwt import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Ads api",
        default_version='v1',
        description="For Azim rest api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="test@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(SessionAuthentication,),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('news.urls')),

    re_path(r"^api/v1/auth/users/sign_in/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^api/v1/auth/token/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^api/v1/auth/token/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
