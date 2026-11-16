from django.urls import path
from . import views, api_views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('event/<slug:slug>/', views.event_detail, name='event-detail'),
    path('category/<slug:category_slug>/', views.events_by_category, name='events-by-category'),

    path('api/events/', api_views.event_list_create_api, name='api-event-list-create'),
    path('api/events/<int:pk>/', api_views.event_detail_api, name='api-event-detail'),
    path('api/categories/', api_views.category_list_api, name='api-category-list'),
    path('api/categories/<int:pk>/', api_views.category_detail_api, name='api-category-detail'),  # Zadanie 1
    path('api/tags/', api_views.tag_list_create_api, name='api-tag-list-create'),                 # Zadanie 2
]