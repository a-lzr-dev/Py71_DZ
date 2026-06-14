from django.urls import path

from . import views

#app_name = "events:api"

urlpatterns = [
    path('api/events/', views.EventListView.as_view(), name='events-list'),
    path('api/events/<int:pk>/', views.SubscribeToEventView.as_view(), name='events-subscribe'),
    path('api/events/my/', views.MyEventsView.as_view(), name='events-my'),
]