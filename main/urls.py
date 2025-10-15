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
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.index, name="index"),
    path("search-plant-name/", views.search_plant_name, name="search-plant-name"),
    path(
        "search-vascan-taxon-id/",
        views.search_vascan_taxon_id,
        name="search-vascan-taxon-id",
    ),
    path(
        "export-plant-search-results/",
        views.export_plant_search_results,
        name="export-plant-search-results",
    ),
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
    path("admin-colour-add/", views.admin_colour_add, name="admin-colour-add"),
    path("admin-colour-page/", views.admin_colour_page, name="admin-colour-page"),
    path(
        "admin-colour-delete/<int:pk>",
        views.admin_colour_delete,
        name="admin-colour-delete",
    ),
    path(
        "admin-colour-update/<int:pk>/",
        views.admin_colour_update,
        name="admin-colour-update",
    ),
]

urlpatterns += [
    path("admin-lifespan-add/", views.admin_lifespan_add, name="admin-lifespan-add"),
    path("admin-lifespan-page/", views.admin_lifespan_page, name="admin-lifespan-page"),
    path(
        "admin-lifespan-delete/<int:pk>",
        views.admin_lifespan_delete,
        name="admin-lifespan-delete",
    ),
    path(
        "admin-lifespan-update/<int:pk>/",
        views.admin_lifespan_update,
        name="admin-lifespan-update",
    ),
]

urlpatterns += [
    path(
        "admin-growth-habit-add/",
        views.admin_growth_habit_add,
        name="admin-growth-habit-add",
    ),
    path(
        "admin-growth-habit-page/",
        views.admin_growth_habit_page,
        name="admin-growth-habit-page",
    ),
    path(
        "admin-growth-habit-delete/<int:pk>",
        views.admin_growth_habit_delete,
        name="admin-growth-habit-delete",
    ),
    path(
        "admin-growth-habit-update/<int:pk>/",
        views.admin_growth_habit_update,
        name="admin-growth-habit-update",
    ),
]

urlpatterns += [
    path(
        "admin-harvesting-indicator-add/",
        views.admin_harvesting_indicator_add,
        name="admin-harvesting-indicator-add",
    ),
    path(
        "admin-harvesting-indicator-page/",
        views.admin_harvesting_indicator_page,
        name="admin-harvesting-indicator-page",
    ),
    path(
        "admin-harvesting-indicator-delete/<int:pk>",
        views.admin_harvesting_indicator_delete,
        name="admin-harvesting-indicator-delete",
    ),
    path(
        "admin-harvesting-indicator-update/<int:pk>/",
        views.admin_harvesting_indicator_update,
        name="admin-harvesting-indicator-update",
    ),
]

urlpatterns += [
    path(
        "admin-harvesting-mean-add/",
        views.admin_harvesting_mean_add,
        name="admin-harvesting-mean-add",
    ),
    path(
        "admin-harvesting-mean-page/",
        views.admin_harvesting_mean_page,
        name="admin-harvesting-mean-page",
    ),
    path(
        "admin-harvesting-mean-delete/<int:pk>",
        views.admin_harvesting_mean_delete,
        name="admin-harvesting-mean-delete",
    ),
    path(
        "admin-harvesting-mean-update/<int:pk>/",
        views.admin_harvesting_mean_update,
        name="admin-harvesting-mean-update",
    ),
]

urlpatterns += [
    path(
        "admin-seed-head-add/",
        views.admin_seed_head_add,
        name="admin-seed-head-add",
    ),
    path(
        "admin-seed-head-page/",
        views.admin_seed_head_page,
        name="admin-seed-head-page",
    ),
    path(
        "admin-seed-head-delete/<int:pk>",
        views.admin_seed_head_delete,
        name="admin-seed-head-delete",
    ),
    path(
        "admin-seed-head-update/<int:pk>/",
        views.admin_seed_head_update,
        name="admin-seed-head-update",
    ),
]

urlpatterns += [
    path(
        "admin-seed-viability-test-add/",
        views.admin_seed_viability_test_add,
        name="admin-seed-viability-test-add",
    ),
    path(
        "admin-seed-viability-test-page/",
        views.admin_seed_viability_test_page,
        name="admin-seed-viability-test-page",
    ),
    path(
        "admin-seed-viability-test-delete/<int:pk>",
        views.admin_seed_viability_test_delete,
        name="admin-seed-viability-test-delete",
    ),
    path(
        "admin-seed-viability-test-update/<int:pk>/",
        views.admin_seed_viability_test_update,
        name="admin-seed-viability-test-update",
    ),
]

urlpatterns += [
    path(
        "admin-seed-storage-add/",
        views.admin_seed_storage_add,
        name="admin-seed-storage-add",
    ),
    path(
        "admin-seed-storage-page/",
        views.admin_seed_storage_page,
        name="admin-seed-storage-page",
    ),
    path(
        "admin-seed-storage-delete/<int:pk>",
        views.admin_seed_storage_delete,
        name="admin-seed-storage-delete",
    ),
    path(
        "admin-seed-storage-update/<int:pk>/",
        views.admin_seed_storage_update,
        name="admin-seed-storage-update",
    ),
]

urlpatterns += [
    path(
        "admin-one-cultivar-add/",
        views.admin_one_cultivar_add,
        name="admin-one-cultivar-add",
    ),
    path(
        "admin-one-cultivar-page/",
        views.admin_one_cultivar_page,
        name="admin-one-cultivar-page",
    ),
    path(
        "admin-one-cultivar-update/<int:pk>/",
        views.admin_one_cultivar_update,
        name="admin-one-cultivar-update",
    ),
    path(
        "admin-one-cultivar-delete/<int:pk>/",
        views.admin_one_cultivar_delete,
        name="admin-one-cultivar-delete",
    ),
]

urlpatterns += [
    path(
        "admin-stratification-duration-add/",
        views.admin_stratification_duration_add,
        name="admin-stratification-duration-add",
    ),
    path(
        "admin-stratification-duration-page/",
        views.admin_stratification_duration_page,
        name="admin-stratification-duration-page",
    ),
    path(
        "admin-stratification-duration-update/<int:pk>/",
        views.admin_stratification_duration_update,
        name="admin-stratification-duration-update",
    ),
    path(
        "admin-stratification-duration-delete/<int:pk>/",
        views.admin_stratification_duration_delete,
        name="admin-stratification-duration-delete",
    ),
]

urlpatterns += [
    path(
        "admin-sowing-depth-add/",
        views.admin_sowing_depth_add,
        name="admin-sowing-depth-add",
    ),
    path(
        "admin-sowing-depth-page/",
        views.admin_sowing_depth_page,
        name="admin-sowing-depth-page",
    ),
    path(
        "admin-sowing-depth-update/<int:pk>/",
        views.admin_sowing_depth_update,
        name="admin-sowing-depth-update",
    ),
    path(
        "admin-sowing-depth-delete/<int:pk>/",
        views.admin_sowing_depth_delete,
        name="admin-sowing-depth-delete",
    ),
]

urlpatterns += [
    path(
        "admin-packaging-measure-add/",
        views.admin_packaging_measure_add,
        name="admin-packaging-measure-add",
    ),
    path(
        "admin-packaging-measure-page/",
        views.admin_packaging_measure_page,
        name="admin-packaging-measure-page",
    ),
    path(
        "admin-packaging-measure-update/<int:pk>/",
        views.admin_packaging_measure_update,
        name="admin-packaging-measure-update",
    ),
    path(
        "admin-packaging-measure-delete/<int:pk>/",
        views.admin_packaging_measure_delete,
        name="admin-packaging-measure-delete",
    ),
]

urlpatterns += [
    path(
        "admin-seed-preparation-add/",
        views.admin_seed_preparation_add,
        name="admin-seed-preparation-add",
    ),
    path(
        "admin-seed-preparation-page/",
        views.admin_seed_preparation_page,
        name="admin-seed-preparation-page",
    ),
    path(
        "admin-seed-preparation-update/<int:pk>/",
        views.admin_seed_preparation_update,
        name="admin-seed-preparation-update",
    ),
    path(
        "admin-seed-preparation-delete/<int:pk>/",
        views.admin_seed_preparation_delete,
        name="admin-seed-preparation-delete",
    ),
]

urlpatterns += [
    path(
        "admin-seed-event-table-add/",
        views.admin_seed_event_table_add,
        name="admin-seed-event-table-add",
    ),
    path(
        "admin-seed-event-table-page/",
        views.admin_seed_event_table_page,
        name="admin-seed-event-table-page",
    ),
    path(
        "admin-seed-event-table-update/<int:pk>/",
        views.admin_seed_event_table_update,
        name="admin-seed-event-table-update",
    ),
    path(
        "admin-seed-event-table-delete/<int:pk>/",
        views.admin_seed_event_table_delete,
        name="admin-seed-event-table-delete",
    ),
]

urlpatterns += [
    path(
        "admin-toxicity-indicator-add/",
        views.admin_toxicity_indicator_add,
        name="admin-toxicity-indicator-add",
    ),
    path(
        "admin-toxicity-indicator-page/",
        views.admin_toxicity_indicator_page,
        name="admin-toxicity-indicator-page",
    ),
    path(
        "admin-toxicity-indicator-update/<int:pk>/",
        views.admin_toxicity_indicator_update,
        name="admin-toxicity-indicator-update",
    ),
    path(
        "admin-toxicity-indicator-delete/<int:pk>/",
        views.admin_toxicity_indicator_delete,
        name="admin-toxicity-indicator-delete",
    ),
]

urlpatterns += [
    path(
        "admin-conservation-status-add/",
        views.admin_conservation_status_add,
        name="admin-conservation-status-add",
    ),
    path(
        "admin-conservation-status-page/",
        views.admin_conservation_status_page,
        name="admin-conservation-status-page",
    ),
    path(
        "admin-conservation-status-update/<int:pk>/",
        views.admin_conservation_status_update,
        name="admin-conservation-status-update",
    ),
    path(
        "admin-conservation-status-delete/<int:pk>/",
        views.admin_conservation_status_delete,
        name="admin-conservation-status-delete",
    ),
]

urlpatterns += [
    path(
        "admin-butterfly-species-page/",
        views.admin_butterfly_species_page,
        name="admin-butterfly-species-page",
    ),
    path(
        "admin-butterfly-species-add/",
        views.admin_butterfly_species_add,
        name="admin-butterfly-species-add",
    ),
    path(
        "admin-butterfly-species-update/<int:pk>/",
        views.admin_butterfly_species_update,
        name="admin-butterfly-species-update",
    ),
    path(
        "admin-butterfly-species-delete/<int:pk>/",
        views.admin_butterfly_species_delete,
        name="admin-butterfly-species-delete",
    ),
]

urlpatterns += [
    path(
        "admin-bee-species-page/",
        views.admin_bee_species_page,
        name="admin-bee-species-page",
    ),
    path(
        "admin-bee-species-add/",
        views.admin_bee_species_add,
        name="admin-bee-species-add",
    ),
    path(
        "admin-bee-species-update/<int:pk>/",
        views.admin_bee_species_update,
        name="admin-bee-species-update",
    ),
    path(
        "admin-bee-species-delete/<int:pk>/",
        views.admin_bee_species_delete,
        name="admin-bee-species-delete",
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
    # path for creating a new plant profile
    path(
        "plant-identification-information-create/",
        views.plant_identification_information_create,
        name="plant-identification-information-create",
    ),
    path(
        "plant-growth-characteristics-update/<int:pk>",
        views.plant_growth_characteristics_update,
        name="plant-growth-characteristics-update",
    ),
    path(
        "plant-introductory-gardening-experience-update/<int:pk>",
        views.plant_introductory_gardening_experience_update,
        name="plant-introductory-gardening-experience-update",
    ),
    path(
        "plant-landscape-use-and-application-update/<int:pk>",
        views.plant_landscape_use_and_application_update,
        name="plant-landscape-use-and-application-update",
    ),
    path(
        "plant-ecological-benefits-update/<int:pk>",
        views.plant_ecological_benefits_update,
        name="plant-ecological-benefits-update",
    ),
    path(
        "plant-special-features-and-considerations-update/<int:pk>",
        views.plant_special_features_and_consideration_update,
        name="plant-special-features-and-considerations-update",
    ),
    path(
        "plant-harvesting-update/<int:pk>",
        views.plant_harvesting_update,
        name="plant-harvesting-update",
    ),
    path(
        "plant-sowing-update/<int:pk>",
        views.plant_sowing_update,
        name="plant-sowing-update",
    ),
    path(
        "plant-seed-distribution-update/<int:pk>",
        views.plant_seed_distribution_update,
        name="plant-seed-distribution-update",
    ),
]

urlpatterns += [
    path(
        "butterfly-supporting-plants/",
        views.butterfly_supporting_plants,
        name="butterfly-supporting-plants",
    ),
    path(
        "bee-supporting-plants/",
        views.bee_supporting_plants,
        name="bee-supporting-plants",
    ),
    path("plant-ecozones/", views.plant_ecozones, name="plant_ecozones"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path("api/v1/", api.urls),
]
