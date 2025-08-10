from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from project import views
from project.api import router as home_router

api = NinjaAPI(version="1.0.0")
api.add_router("/", home_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.index, name="index"),
    path("search-plant/", views.advanced_search_plant, name="search-plant"),
    path("search-plant-name/", views.search_plant_name, name="search-plant-name"),
    path(
        "plant-catalogue-intro/",
        views.plant_catalogue_intro,
        name="plant-catalogue-intro",
    ),
    path("update-availability/", views.update_availability, name="update-availability"),
    path(
        "toggle-availability/<int:pk>",
        views.toggle_availability,
        name="toggle-availability",
    ),
    path("plant-catalog/", views.plant_catalog, name="plant-catalog"),
]
urlpatterns += [
    path(
        "plant-profile-page/<int:pk>",
        views.plant_profile_page,
        name="plant-profile-page",
    ),
    path("plant-profile-add/", views.plant_profile_add, name="plant-profile-add"),
    path(
        "plant-profile-delete/<int:pk>",
        views.plant_profile_delete,
        name="plant-profile-delete",
    ),
    path(
        "plant-profile-update/<int:pk>",
        views.plant_profile_update,
        name="plant-profile-update",
    ),
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
    path(
        "harvesting-indicator-add/",
        views.harvesting_indicator_add,
        name="harvesting-indicator-add",
    ),
    path(
        "harvesting-indicator-table/",
        views.harvesting_indicator_table,
        name="harvesting-indicator-table",
    ),
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
    path(
        "harvesting-mean-table/",
        views.harvesting_mean_table,
        name="harvesting-mean-table",
    ),
    path(
        "harvesting-mean-delete/<int:pk>",
        views.harvesting_mean_delete,
        name="harvesting-mean-delete",
    ),
    path(
        "harvesting-mean-update/<int:pk>/",
        views.harvesting_mean_update,
        name="harvesting-mean-update",
    ),
]

urlpatterns += [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path(
        "user-plant-collection/",
        views.user_plant_collection,
        name="user-plant-collection",
    ),
    path(
        "user-plant-toggle/<int:pk>", views.user_plant_toggle, name="user-plant-toggle"
    ),
    path(
        "user-plant-update/<int:pk>", views.user_plant_update, name="user-plant-update"
    ),
    path(
        "user-plant-delete/<int:pk>", views.user_plant_delete, name="user-plant-delete"
    ),
    path(
        "plant-collection-csv/", views.plant_collection_csv, name="plant-collection-csv"
    ),
    path("site-admin/", views.siteadmin, name="site-admin"),
]

urlpatterns += [
    path("plant-label-pdf/<int:pk>", views.plant_label_pdf, name="plant-label-pdf"),
]
urlpatterns += [
    path(
        "plant-environmental-requirement-update/<int:pk>",
        views.plant_environmental_requirement_update,
        name="plant-environmental-requirement-update",
    ),
    path(
        "plant-identification-information-update/<int:pk>",
        views.plant_identification_information_update,
        name="plant-identification-information-update",
    ),
    path(
        "plant-growth-characteristics-update/<int:pk>",
        views.plant_growth_characteristics_update,
        name="plant-growth-characteristics-update",
    ),
    path(
        "plant-propagation-and-seed-sharing-update/<int:pk>",
        views.plant_propagation_and_seed_sharing_update,
        name="plant-propagation-and-seed-sharing-update",
    ),
]

urlpatterns += [
    path(
        "butterfly-supporting-plants/",
        views.butterfly_supporting_plants,
        name="butterfly-supporting-plants",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path("api/v1/", api.urls),
]
