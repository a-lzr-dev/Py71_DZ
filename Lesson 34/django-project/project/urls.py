"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounting import views as accounting_views
from events import views as events_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", events_views.home_view, name="home"),
    path("about", events_views.about_view, name="about"),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/auth/", include("djoser.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path('', include('accounting.api.urls')),
    path('', include('events.api.urls')),
    path("register", accounting_views.register_user_view, name="accounting-register"),
    path("login", accounting_views.CustomLoginView.as_view(), name="accounting-login"),
    path("logout", LogoutView.as_view(), name="accounting-logout"),
]

urlpatterns += debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)