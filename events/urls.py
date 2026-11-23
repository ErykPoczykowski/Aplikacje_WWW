from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, cbv_views
from .viewsets import CategoryViewSet, EventViewSet

app_name = 'events'

# Inicjalizujemy router i rejestrujemy nasze ViewSety (generuje trasy względne: categories/, events/...)
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    # 1. Tradycyjne widoki HTML (MVT) z Lab 3
    path('', views.event_list, name='event-list'),
    path('event/<slug:slug>/', views.event_detail, name='event-detail'),
    path('category/<slug:category_slug>/', views.events_by_category, name='events-by-category'),

    # 2. Endpointy widoków generycznych CBV (porównawczo)
    path('api/cbv/events/', cbv_views.EventListCreateGenericView.as_view(), name='generic-event-list'),
    path('api/cbv/events/<int:pk>/', cbv_views.EventRetrieveUpdateDestroyGenericView.as_view(), name='generic-event-detail'),

    # 3. Profesjonalne REST API oparte na ViewSets i Routerze osadzone pod prefiksem wersji v1
    # Wszystkie trasy z routera otrzymują tu prefiks 'api/v1/' -> np. /events/api/v1/events/
    path('api/v1/', include(router.urls)),
]