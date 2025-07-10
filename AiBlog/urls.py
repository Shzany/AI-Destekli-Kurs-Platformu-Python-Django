from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from pages.sitemaps import StaticViewSitemap, PageSitemap
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Dokümantasyonu",
      default_version='v1',
      description="Swagger arayüzü",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

sitemaps = {
    'static': StaticViewSitemap,
    'pages': PageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path("user/",include('user.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('pages.urls')), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]