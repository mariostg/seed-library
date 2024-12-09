from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
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

urlpatterns += [
    path("color-add/", views.color_add, name="color-add"),
    path("color-table/", views.color_table, name="color-table"),
    path("color-delete/<int:pk>", views.color_delete, name="color-delete"),
    path("color-update/<int:pk>/", views.color_update, name="color-update"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
