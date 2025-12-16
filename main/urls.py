from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from ninja import NinjaAPI

from project import views
from project.api import router as home_router

api = NinjaAPI(version="1.0.0")
api.add_router("/", home_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += i18n_patterns(
    path("en/", include("django.contrib.auth.urls")),
    path("fr/", include("django.contrib.auth.urls")),
    path("", views.index, name="index"),
    path(_("search-plant-name/"), views.search_plant_name, name="search-plant-name"),
    path(
        _("search-plant-images/"), views.search_plant_images, name="search-plant-images"
    ),
    path(
        _("search-vascan-taxon-id/"),
        views.search_vascan_taxon_id,
        name="search-vascan-taxon-id",
    ),
    path(
        _("export-plant-search-results/"),
        views.export_plant_search_results,
        name="export-plant-search-results",
    ),
    path(
        _("plant-catalogue-intro/"),
        views.plant_catalogue_intro,
        name="plant-catalogue-intro",
    ),
    path(
        _("update-availability/"), views.update_availability, name="update-availability"
    ),
    path(
        _("toggle-availability/<int:pk>"),
        views.toggle_availability,
        name="toggle-availability",
    ),
    path(
        _("toggle-is-active/<int:pk>"), views.toggle_is_active, name="toggle-is-active"
    ),
    path(
        _("toggle-seed-accepting/<int:pk>"),
        views.toggle_seed_accepting,
        name="toggle-seed-accepting",
    ),
    path(
        _("toggle-seed-needed/<int:pk>"),
        views.toggle_seed_needed,
        name="toggle-seed-needed",
    ),
    path(
        _("toggle-plant-accepted/<int:pk>"),
        views.toggle_plant_accepted,
        name="toggle-plant-accepted",
    ),
    path(_("plant-catalog/"), views.plant_catalog, name="plant-catalog"),
)

urlpatterns += i18n_patterns(
    path(
        _("plant-profile-page/<int:pk>"),
        views.plant_profile_page,
        name="plant-profile-page",
    ),
    path(
        _("plant-profile-delete/<int:pk>"),
        views.plant_profile_delete,
        name="plant-profile-delete",
    ),
    path(
        _("plant-profile-update/<int:pk>"),
        views.plant_profile_update,
        name="plant-profile-update",
    ),
    path(
        _("plant-profile-images/<int:pk>"),
        views.plant_profile_images,
        name="plant-profile-images",
    ),
    path(
        _("plant-seed-box-label-pdf/<int:pk>"),
        views.plant_seed_box_label_pdf,
        name="plant-seed-box-label-pdf",
    ),
)


urlpatterns += i18n_patterns(
    path(
        _("admin-accept-all-seeds/"),
        views.admin_accept_all_seeds,
        name="admin-accept-all-seeds",
    ),
    path(
        _("admin-refuse-all-seeds/"),
        views.admin_refuse_all_seeds,
        name="admin-refuse-all-seeds",
    ),
)

urlpatterns += i18n_patterns(
    path(_("admin-colour-add/"), views.admin_colour_add, name="admin-colour-add"),
    path(_("admin-colour-page/"), views.admin_colour_page, name="admin-colour-page"),
    path(
        _("admin-colour-delete/<int:pk>"),
        views.admin_colour_delete,
        name="admin-colour-delete",
    ),
    path(
        _("admin-colour-update/<int:pk>/"),
        views.admin_colour_update,
        name="admin-colour-update",
    ),
)

urlpatterns += i18n_patterns(
    path(_("admin-lifespan-add/"), views.admin_lifespan_add, name="admin-lifespan-add"),
    path(
        _("admin-lifespan-page/"), views.admin_lifespan_page, name="admin-lifespan-page"
    ),
    path(
        _("admin-lifespan-delete/<int:pk>"),
        views.admin_lifespan_delete,
        name="admin-lifespan-delete",
    ),
    path(
        _("admin-lifespan-update/<int:pk>/"),
        views.admin_lifespan_update,
        name="admin-lifespan-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-growth-habit-add/"),
        views.admin_growth_habit_add,
        name="admin-growth-habit-add",
    ),
    path(
        _("admin-growth-habit-page/"),
        views.admin_growth_habit_page,
        name="admin-growth-habit-page",
    ),
    path(
        _("admin-growth-habit-delete/<int:pk>"),
        views.admin_growth_habit_delete,
        name="admin-growth-habit-delete",
    ),
    path(
        _("admin-growth-habit-update/<int:pk>/"),
        views.admin_growth_habit_update,
        name="admin-growth-habit-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-harvesting-indicator-add/"),
        views.admin_harvesting_indicator_add,
        name="admin-harvesting-indicator-add",
    ),
    path(
        _("admin-harvesting-indicator-page/"),
        views.admin_harvesting_indicator_page,
        name="admin-harvesting-indicator-page",
    ),
    path(
        _("admin-harvesting-indicator-delete/<int:pk>"),
        views.admin_harvesting_indicator_delete,
        name="admin-harvesting-indicator-delete",
    ),
    path(
        _("admin-harvesting-indicator-update/<int:pk>/"),
        views.admin_harvesting_indicator_update,
        name="admin-harvesting-indicator-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-harvesting-mean-add/"),
        views.admin_harvesting_mean_add,
        name="admin-harvesting-mean-add",
    ),
    path(
        _("admin-harvesting-mean-page/"),
        views.admin_harvesting_mean_page,
        name="admin-harvesting-mean-page",
    ),
    path(
        _("admin-harvesting-mean-delete/<int:pk>"),
        views.admin_harvesting_mean_delete,
        name="admin-harvesting-mean-delete",
    ),
    path(
        _("admin-harvesting-mean-update/<int:pk>/"),
        views.admin_harvesting_mean_update,
        name="admin-harvesting-mean-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-seed-head-add/"),
        views.admin_seed_head_add,
        name="admin-seed-head-add",
    ),
    path(
        _("admin-seed-head-page/"),
        views.admin_seed_head_page,
        name="admin-seed-head-page",
    ),
    path(
        _("admin-seed-head-delete/<int:pk>"),
        views.admin_seed_head_delete,
        name="admin-seed-head-delete",
    ),
    path(
        _("admin-seed-head-update/<int:pk>/"),
        views.admin_seed_head_update,
        name="admin-seed-head-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-seed-viability-test-add/"),
        views.admin_seed_viability_test_add,
        name="admin-seed-viability-test-add",
    ),
    path(
        _("admin-seed-viability-test-page/"),
        views.admin_seed_viability_test_page,
        name="admin-seed-viability-test-page",
    ),
    path(
        _("admin-seed-viability-test-delete/<int:pk>"),
        views.admin_seed_viability_test_delete,
        name="admin-seed-viability-test-delete",
    ),
    path(
        _("admin-seed-viability-test-update/<int:pk>/"),
        views.admin_seed_viability_test_update,
        name="admin-seed-viability-test-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-seed-storage-add/"),
        views.admin_seed_storage_add,
        name="admin-seed-storage-add",
    ),
    path(
        _("admin-seed-storage-page/"),
        views.admin_seed_storage_page,
        name="admin-seed-storage-page",
    ),
    path(
        _("admin-seed-storage-delete/<int:pk>"),
        views.admin_seed_storage_delete,
        name="admin-seed-storage-delete",
    ),
    path(
        _("admin-seed-storage-update/<int:pk>/"),
        views.admin_seed_storage_update,
        name="admin-seed-storage-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-one-cultivar-add/"),
        views.admin_one_cultivar_add,
        name="admin-one-cultivar-add",
    ),
    path(
        _("admin-one-cultivar-page/"),
        views.admin_one_cultivar_page,
        name="admin-one-cultivar-page",
    ),
    path(
        _("admin-one-cultivar-update/<int:pk>/"),
        views.admin_one_cultivar_update,
        name="admin-one-cultivar-update",
    ),
    path(
        _("admin-one-cultivar-delete/<int:pk>/"),
        views.admin_one_cultivar_delete,
        name="admin-one-cultivar-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-stratification-duration-add/"),
        views.admin_stratification_duration_add,
        name="admin-stratification-duration-add",
    ),
    path(
        _("admin-stratification-duration-page/"),
        views.admin_stratification_duration_page,
        name="admin-stratification-duration-page",
    ),
    path(
        _("admin-stratification-duration-update/<int:pk>/"),
        views.admin_stratification_duration_update,
        name="admin-stratification-duration-update",
    ),
    path(
        _("admin-stratification-duration-delete/<int:pk>/"),
        views.admin_stratification_duration_delete,
        name="admin-stratification-duration-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-sowing-depth-add/"),
        views.admin_sowing_depth_add,
        name="admin-sowing-depth-add",
    ),
    path(
        _("admin-sowing-depth-page/"),
        views.admin_sowing_depth_page,
        name="admin-sowing-depth-page",
    ),
    path(
        _("admin-sowing-depth-update/<int:pk>/"),
        views.admin_sowing_depth_update,
        name="admin-sowing-depth-update",
    ),
    path(
        _("admin-sowing-depth-delete/<int:pk>/"),
        views.admin_sowing_depth_delete,
        name="admin-sowing-depth-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-packaging-measure-add/"),
        views.admin_packaging_measure_add,
        name="admin-packaging-measure-add",
    ),
    path(
        _("admin-packaging-measure-page/"),
        views.admin_packaging_measure_page,
        name="admin-packaging-measure-page",
    ),
    path(
        _("admin-packaging-measure-update/<int:pk>/"),
        views.admin_packaging_measure_update,
        name="admin-packaging-measure-update",
    ),
    path(
        _("admin-packaging-measure-delete/<int:pk>/"),
        views.admin_packaging_measure_delete,
        name="admin-packaging-measure-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-seed-preparation-add/"),
        views.admin_seed_preparation_add,
        name="admin-seed-preparation-add",
    ),
    path(
        _("admin-seed-preparation-page/"),
        views.admin_seed_preparation_page,
        name="admin-seed-preparation-page",
    ),
    path(
        _("admin-seed-preparation-update/<int:pk>/"),
        views.admin_seed_preparation_update,
        name="admin-seed-preparation-update",
    ),
    path(
        _("admin-seed-preparation-delete/<int:pk>/"),
        views.admin_seed_preparation_delete,
        name="admin-seed-preparation-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-seed-event-table-add/"),
        views.admin_seed_event_table_add,
        name="admin-seed-event-table-add",
    ),
    path(
        _("admin-seed-event-table-page/"),
        views.admin_seed_event_table_page,
        name="admin-seed-event-table-page",
    ),
    path(
        _("admin-seed-event-table-update/<int:pk>/"),
        views.admin_seed_event_table_update,
        name="admin-seed-event-table-update",
    ),
    path(
        _("admin-seed-event-table-delete/<int:pk>/"),
        views.admin_seed_event_table_delete,
        name="admin-seed-event-table-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-toxicity-indicator-add/"),
        views.admin_toxicity_indicator_add,
        name="admin-toxicity-indicator-add",
    ),
    path(
        _("admin-toxicity-indicator-page/"),
        views.admin_toxicity_indicator_page,
        name="admin-toxicity-indicator-page",
    ),
    path(
        _("admin-toxicity-indicator-update/<int:pk>/"),
        views.admin_toxicity_indicator_update,
        name="admin-toxicity-indicator-update",
    ),
    path(
        _("admin-toxicity-indicator-delete/<int:pk>/"),
        views.admin_toxicity_indicator_delete,
        name="admin-toxicity-indicator-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-conservation-status-add/"),
        views.admin_conservation_status_add,
        name="admin-conservation-status-add",
    ),
    path(
        _("admin-conservation-status-page/"),
        views.admin_conservation_status_page,
        name="admin-conservation-status-page",
    ),
    path(
        _("admin-conservation-status-update/<int:pk>/"),
        views.admin_conservation_status_update,
        name="admin-conservation-status-update",
    ),
    path(
        _("admin-conservation-status-delete/<int:pk>/"),
        views.admin_conservation_status_delete,
        name="admin-conservation-status-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-butterfly-species-page/"),
        views.admin_butterfly_species_page,
        name="admin-butterfly-species-page",
    ),
    path(
        _("admin-butterfly-species-add/"),
        views.admin_butterfly_species_add,
        name="admin-butterfly-species-add",
    ),
    path(
        _("admin-butterfly-species-update/<int:pk>/"),
        views.admin_butterfly_species_update,
        name="admin-butterfly-species-update",
    ),
    path(
        _("admin-butterfly-species-delete/<int:pk>/"),
        views.admin_butterfly_species_delete,
        name="admin-butterfly-species-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-bee-species-page/"),
        views.admin_bee_species_page,
        name="admin-bee-species-page",
    ),
    path(
        _("admin-bee-species-add/"),
        views.admin_bee_species_add,
        name="admin-bee-species-add",
    ),
    path(
        _("admin-bee-species-update/<int:pk>/"),
        views.admin_bee_species_update,
        name="admin-bee-species-update",
    ),
    path(
        _("admin-bee-species-delete/<int:pk>/"),
        views.admin_bee_species_delete,
        name="admin-bee-species-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-non-native-species-page/"),
        views.admin_non_native_species_page,
        name="admin-non-native-species-page",
    ),
    path(
        _("admin-non-native-species-add/"),
        views.admin_non_native_species_add,
        name="admin-non-native-species-add",
    ),
    path(
        _("admin-non-native-species-update/<int:pk>/"),
        views.admin_non_native_species_update,
        name="admin-non-native-species-update",
    ),
    path(
        _("admin-non-native-species-delete/<int:pk>/"),
        views.admin_non_native_species_delete,
        name="admin-non-native-species-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(_("admin-ecozone-page/"), views.admin_ecozone_page, name="admin-ecozone-page"),
    path(
        _("admin-ecozone-add/"),
        views.admin_ecozone_add,
        name="admin-ecozone-add",
    ),
    path(
        _("admin-ecozone-update/<int:pk>/"),
        views.admin_ecozone_update,
        name="admin-ecozone-update",
    ),
    path(
        _("admin-ecozone-delete/<int:pk>/"),
        views.admin_ecozone_delete,
        name="admin-ecozone-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(_("admin-images-page/"), views.admin_images_page, name="admin-images-page"),
    path(_("admin-image-add/"), views.admin_image_add, name="admin-image-add"),
    path(
        _("admin-image-update/<int:pk>/"),
        views.admin_image_update,
        name="admin-image-update",
    ),
    path(
        _("admin-image-delete/<int:pk>/"),
        views.admin_image_delete,
        name="admin-image-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("admin-plant-morphology-page/"),
        views.admin_plant_morphology_page,
        name="admin-plant-morphology-page",
    ),
    path(
        _("admin-plant-morphology-add/"),
        views.admin_plant_morphology_add,
        name="admin-plant-morphology-add",
    ),
    path(
        _("admin-plant-morphology-update/<int:pk>/"),
        views.admin_plant_morphology_update,
        name="admin-plant-morphology-update",
    ),
    path(
        _("admin-plant-morphology-delete/<int:pk>/"),
        views.admin_plant_morphology_delete,
        name="admin-plant-morphology-delete",
    ),
)

urlpatterns += i18n_patterns(
    path(_("login/"), views.user_login, name="login"),
    path(_("logout/"), views.user_logout, name="logout"),
    path(
        _("user-plant-collection/"),
        views.user_plant_collection,
        name="user-plant-collection",
    ),
    path(
        _("user-plant-toggle/<int:pk>"),
        views.user_plant_toggle,
        name="user-plant-toggle",
    ),
    path(
        _("user-plant-update/<int:pk>"),
        views.user_plant_update,
        name="user-plant-update",
    ),
    path(
        _("user-plant-delete/<int:pk>"),
        views.user_plant_delete,
        name="user-plant-delete",
    ),
    path(
        _("plant-collection-csv/"),
        views.plant_collection_csv,
        name="plant-collection-csv",
    ),
    path(_("site-admin/"), views.siteadmin, name="site-admin"),
)

urlpatterns += i18n_patterns(
    path(_("plant-label-pdf/<int:pk>"), views.plant_label_pdf, name="plant-label-pdf"),
)

urlpatterns += i18n_patterns(
    path(
        _("plant-environmental-requirement-update/<int:pk>"),
        views.plant_environmental_requirement_update,
        name="plant-environmental-requirement-update",
    ),
    path(
        _("plant-identification-information-update/<int:pk>"),
        views.plant_identification_information_update,
        name="plant-identification-information-update",
    ),
    # path for creating a new plant profile
    path(
        _("plant-identification-information-create/"),
        views.plant_identification_information_create,
        name="plant-identification-information-create",
    ),
    # path for plants missingq inat taxon
    path(
        _("admin-plant-missing-inaturalist-taxon/"),
        views.admin_plant_missing_inaturalist_taxon,
        name="admin-plant-missing-inaturalist-taxon",
    ),
    path(
        _("plant-growth-characteristics-update/<int:pk>"),
        views.plant_growth_characteristics_update,
        name="plant-growth-characteristics-update",
    ),
    path(
        _("plant-introductory-gardening-experience-update/<int:pk>"),
        views.plant_introductory_gardening_experience_update,
        name="plant-introductory-gardening-experience-update",
    ),
    path(
        _("plant-landscape-use-and-application-update/<int:pk>"),
        views.plant_landscape_use_and_application_update,
        name="plant-landscape-use-and-application-update",
    ),
    path(
        _("plant-ecological-benefits-update/<int:pk>"),
        views.plant_ecological_benefits_update,
        name="plant-ecological-benefits-update",
    ),
    path(
        _("plant-special-features-and-considerations-update/<int:pk>"),
        views.plant_special_features_and_consideration_update,
        name="plant-special-features-and-considerations-update",
    ),
    path(
        _("plant-harvesting-update/<int:pk>"),
        views.plant_harvesting_update,
        name="plant-harvesting-update",
    ),
    path(
        _("plant-sowing-update/<int:pk>"),
        views.plant_sowing_update,
        name="plant-sowing-update",
    ),
    path(
        _("plant-seed-distribution-update/<int:pk>"),
        views.plant_seed_distribution_update,
        name="plant-seed-distribution-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("plant-substitute-to-update/<int:pk>"),
        views.plant_substitute_to_update,
        name="plant-substitute-to-update",
    ),
)

urlpatterns += i18n_patterns(
    path(
        _("butterfly-supporting-plants/"),
        views.butterfly_supporting_plants,
        name="butterfly-supporting-plants",
    ),
    path(
        _("bee-supporting-plants/"),
        views.bee_supporting_plants,
        name="bee-supporting-plants",
    ),
    path(_("plant-ecozones/"), views.plant_ecozones, name="plant_ecozones"),
    path(
        _("plants-needing-seeds-csv/"),
        views.plants_needing_seeds_csv,
        name="plants-needing-seeds-csv",
    ),
)


urlpatterns += i18n_patterns(
    path(
        _("project-user-page/"),
        views.project_user_page,
        name="project-user-page",
    ),
    path(
        _("project-user-add/"),
        views.project_user_add,
        name="project-user-add",
    ),
    path(
        _("project-user-update/<int:pk>/"),
        views.project_user_update,
        name="project-user-update",
    ),
    path(
        _("project-user-delete/<int:pk>/"),
        views.project_user_delete,
        name="project-user-delete",
    ),
    path(
        _("project-user-groups-update/<int:pk>/"),
        views.project_user_groups_update,
        name="project-user-groups-update",
    ),
    path(
        _("project-user-groups-delete/<int:user_pk>/<int:group_pk>/"),
        views.project_user_groups_delete,
        name="project-user-groups-delete",
    ),
    path(
        _("group-permissions-matrix-update/"),
        views.group_permissions_matrix_update,
        name="group-permissions-matrix-update",
    ),
)


urlpatterns += i18n_patterns(
    path(
        _("project-group-page/"),
        views.project_group_page,
        name="project-group-page",
    ),
    path(
        _("project-group-add/"),
        views.project_group_add,
        name="project-group-add",
    ),
    path(
        _("project-group-update/<int:pk>/"),
        views.project_group_update,
        name="project-group-update",
    ),
    path(
        _("project-group-delete/<int:pk>/"),
        views.project_group_delete,
        name="project-group-delete",
    ),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path("api/v1/", api.urls),
)
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [path("rosetta/", include("rosetta.urls"))]
