from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PageViewset, RateListCreateView
from .serializers import PageSerializer

router = DefaultRouter()
router.register(r'pages', PageViewset)

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('courses/<str:language>/', views.show_language_page, name='language_page'),
    path('courses/<str:language>/<slug:slug>/', views.get_language_detail, name='language_detail'),
    path('courses/<str:category>/<str:slug>/delete/', views.delete_page, name='delete_page'),
    path('search/', views.search, name='search'),
    path('page/edit/<int:page_id>/', views.edit_page, name='edit_page'),
    path('page/save/<int:page_id>/', views.save_page, name='save_page'),
    path('api/pages/<int:page_id>/delete/', views.delete_page, name='delete_page'),
    path('rates/', RateListCreateView.as_view(), name='rate-list-create'),
    path('pages/<int:page_id>/rates/', RateListCreateView.as_view(), name='page-rate-list-create'),
    path('pages/<int:page_id>/rate/', views.add_rate, name='add_rate'),  # Yeni rate ekleme yolu
    path('courses/<str:language>/content/<slug:slug>/', views.get_page_content, name='get_page_content'),
    path('', include(router.urls)),
    # Örnek: page_detail.html
]
