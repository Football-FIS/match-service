from django.contrib import admin
from django.urls import path, re_path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Match Service API",
      default_version='v1',
      description="It's a microservice from footmatch app, a project from University of Seville.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="trabajofis2022@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('match/list', views.MatchViewSet.as_view({'get':'list'})),
    path('match/', views.MatchViewSet.as_view({'post':'create'})),
    path('match/<pk>', views.MatchViewSet.as_view({'get':'get', 'put':'update', 'delete':'delete'})),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]