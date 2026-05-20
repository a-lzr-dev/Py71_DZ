from django.urls import path

from . import views

app_name = "events:api"

urlpatterns = [
    path('api/users/', views.UserRegistrationView.as_view(), name='users-register'),
    path('api/users/list/', views.UserListView.as_view(), name='users-list'),
]