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
    path("update-availability/", views.update_availability, name="update-availability"),
    path("toggle-availability/<int:pk>", views.toggle_availability, name="toggle-availability"),
]
urlpatterns += [
    path("plant-profile-page/<int:pk>", views.plant_profile_page, name="plant-profile-page"),
    path("plant-profile-add/", views.plant_profile_add, name="plant-profile-add"),
    path("plant-profile-update/<int:pk>", views.plant_profile_update, name="plant-profile-update"),
]
urlpatterns += [
    path("color-add/", views.color_add, name="color-add"),
    path("color-table/", views.color_table, name="color-table"),
    path("color-delete/<int:pk>", views.color_delete, name="color-delete"),
    path("color-update/<int:pk>/", views.color_update, name="color-update"),
]

urlpatterns += [
    path("dormancy-add/", views.dormancy_add, name="dormancy-add"),
    path("dormancy-table/", views.dormancy_table, name="dormancy-table"),
    path("dormancy-delete/<int:pk>", views.dormancy_delete, name="dormancy-delete"),
    path("dormancy-update/<int:pk>/", views.habit_update, name="dormancy-update"),
]

urlpatterns += [
    path("habit-add/", views.habit_add, name="habit-add"),
    path("habit-table/", views.habit_table, name="habit-table"),
    path("habit-delete/<int:pk>", views.habit_delete, name="habit-delete"),
    path("habit-update/<int:pk>/", views.habit_update, name="habit-update"),
]

urlpatterns += [
    path("harvesting-indicator-add/", views.harvesting_indicator_add, name="harvesting-indicator-add"),
    path("harvesting-indicator-table/", views.harvesting_indicator_table, name="harvesting-indicator-table"),
    path(
        "harvesting-indicator-delete/<int:pk>",
        views.harvesting_indicator_delete,
        name="harvesting-indicator-delete",
    ),
    path(
        "harvesting-indicator-update/<int:pk>/",
        views.harvesting_indicator_update,
        name="harvesting-indicator-update",
    ),
]

urlpatterns += [
    path("harvesting-mean-add/", views.harvesting_mean_add, name="harvesting-mean-add"),
    path("harvesting-mean-table/", views.harvesting_mean_table, name="harvesting-mean-table"),
    path("harvesting-mean-delete/<int:pk>", views.harvesting_mean_delete, name="harvesting-mean-delete"),
    path("harvesting-mean-update/<int:pk>/", views.harvesting_mean_update, name="harvesting-mean-update"),
]

urlpatterns += [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("site-admin/", views.siteadmin, name="site-admin"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
