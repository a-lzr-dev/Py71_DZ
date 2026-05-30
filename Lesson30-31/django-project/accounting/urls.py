from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "accounting"

urlpatterns = [
    path("register", views.register_user_view, name="register"),
    path("login", views.CustomLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path('password-reset/', views.password_reset_request, name='password-reset'),
#    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
#    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),
]
