from django.contrib import admin
from django.urls import include, path

from project import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.index, name="index"),
    path("search-plant/", views.search_plant, name="search-plant"),
    path("single-plant/<int:pk>", views.single_plant, name="single-plant"),
    path("update-availability/", views.update_availability, name="update-availability"),
    path("toggle-availability/<int:pk>", views.toggle_availability, name="toggle-availability"),
]
