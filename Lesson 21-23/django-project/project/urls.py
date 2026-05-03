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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from accounting import views as accounting_views
from table_reservation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home_view, name="home"),
    path("about", views.about_view, name="about"),
    path("tables", views.TablesListView.as_view(), name="tables-list"),
    path("reservations/my", views.ReservationsListView.as_view(), name="reservations-list"),
    path("reservations/new", views.reservation_create_view, name="reservation-create"),
    path("reservations/new/<int:table_id>", views.reservation_create_view, name="reservation-create"),
    path("reservations/<int:reservation_id>", views.reservation_detail_view, name="reservation-detail"),
#    path("notes", views.notes_list_view, name="notes-list"),
#    path("notes/create", views.note_create_view, name="notes-create"),
#    path("notes/<int:note_id>", views.note_detail_view, name="notes-detail"),
    path("register", accounting_views.register_user_view, name="accounting-register"),
    path("login", accounting_views.CustomLoginView.as_view(), name="accounting-login"),
    path("logout", LogoutView.as_view(), name="accounting-logout"),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)