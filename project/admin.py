import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum
from django.http import HttpResponse

from project import models

# class HarvestingPeriodFilter(admin.SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = "Harvesting Period"

#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = "period"

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return [
#             ("7", "july"),
#             ("8", "aug"),
#         ]

#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         return queryset.filter(
#             harvest_start__gte=6,
#             harvest_end__lte=8,
#         )


class PlantProfileAdmin(admin.ModelAdmin):
    # list_filter = ["harvest_start",]
    search_fields = ["latin_name", "french_name"]


@admin.register(models.Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "status",
        "amount",
        "currency",
        "is_recurring",
        "donor_email",
        "stripe_checkout_session_id",
        "stripe_invoice_id",
        "paid_at",
        "created",
    ]
    list_filter = ["status", "is_recurring", "currency", "created", "paid_at"]
    search_fields = [
        "donor_email",
        "donor_name",
        "stripe_checkout_session_id",
        "stripe_payment_intent_id",
        "stripe_subscription_id",
        "stripe_customer_id",
        "stripe_invoice_id",
    ]
    readonly_fields = ["created", "modified", "paid_at"]
    ordering = ["-created"]
    actions = ["export_selected_as_csv"]
    change_list_template = "admin/project/donation/change_list.html"

    @admin.action(description="Export selected donations as CSV")
    def export_selected_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="donations-export.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "id",
                "status",
                "amount",
                "currency",
                "is_recurring",
                "donor_email",
                "donor_name",
                "stripe_checkout_session_id",
                "stripe_invoice_id",
                "stripe_subscription_id",
                "stripe_payment_intent_id",
                "paid_at",
                "created",
            ]
        )

        for donation in queryset.order_by("-created"):
            writer.writerow(
                [
                    donation.id,
                    donation.status,
                    donation.amount,
                    donation.currency,
                    donation.is_recurring,
                    donation.donor_email,
                    donation.donor_name,
                    donation.stripe_checkout_session_id,
                    donation.stripe_invoice_id,
                    donation.stripe_subscription_id,
                    donation.stripe_payment_intent_id,
                    donation.paid_at,
                    donation.created,
                ]
            )

        return response

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        if not hasattr(response, "context_data") or "cl" not in response.context_data:
            return response

        queryset = response.context_data["cl"].queryset
        aggregates = queryset.aggregate(
            total_amount=Sum("amount"),
            recurring_amount=Sum("amount", filter=Q(is_recurring=True)),
            one_time_amount=Sum("amount", filter=Q(is_recurring=False)),
        )
        response.context_data["donation_totals"] = {
            "count": queryset.count(),
            "total_amount": aggregates["total_amount"] or 0,
            "recurring_amount": aggregates["recurring_amount"] or 0,
            "one_time_amount": aggregates["one_time_amount"] or 0,
        }
        return response


@admin.register(models.StripeWebhookEvent)
class StripeWebhookEventAdmin(admin.ModelAdmin):
    list_display = [
        "stripe_event_id",
        "event_type",
        "livemode",
        "created",
        "has_processing_error",
    ]
    list_filter = ["event_type", "livemode", "created"]
    search_fields = ["stripe_event_id", "event_type", "processing_error"]
    readonly_fields = [
        "stripe_event_id",
        "event_type",
        "livemode",
        "payload",
        "processing_error",
        "created",
        "modified",
    ]
    ordering = ["-created"]
    actions = ["export_selected_as_csv"]

    @admin.display(boolean=True)
    def has_processing_error(self, obj):
        return bool(obj.processing_error)

    @admin.action(description="Export selected webhook events as CSV")
    def export_selected_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="stripe-webhook-events-export.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "stripe_event_id",
                "event_type",
                "livemode",
                "processing_error",
                "created",
                "modified",
            ]
        )

        for event in queryset.order_by("-created"):
            writer.writerow(
                [
                    event.stripe_event_id,
                    event.event_type,
                    event.livemode,
                    event.processing_error,
                    event.created,
                    event.modified,
                ]
            )

        return response

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        # Keep records immutable as an audit trail while still viewable in admin.
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            return False
        return super().has_change_permission(request, obj)


admin.site.register(Permission)


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    # list_display = ["app_label", "model"]
    list_filter = ["app_label"]
    search_fields = ["app_label", "model"]
    ordering = ["app_label", "model"]


admin.site.register(models.PlantProfile, PlantProfileAdmin)
admin.site.register(models.HarvestingIndicator)
admin.site.register(models.HarvestingMean)
admin.site.register(models.SeedHead)
admin.site.register(models.SeedViabilityTest)
admin.site.register(models.SeedStorage)
admin.site.register(models.OneCultivar)
admin.site.register(models.PackagingMeasure)
admin.site.register(models.SeedPreparation)
admin.site.register(models.SeedStorageLabelInfo)
admin.site.register(models.Lighting)
admin.site.register(models.PlantLifespan)
admin.site.register(models.BloomColour)
admin.site.register(models.GrowthHabit)
admin.site.register(models.SowingDepth)
admin.site.register(models.ProjectUser, UserAdmin)
admin.site.register(models.PlantCollection)
admin.site.register(models.PlantImage)
admin.site.register(models.PlantMorphology)
admin.site.register(models.ConservationStatus)
admin.site.register(models.SeedEventTable)
admin.site.register(models.ToxicityIndicator)
admin.site.register(models.ButterflySpecies)
admin.site.register(models.ObsoleteNames)
admin.site.register(models.PlantComplementary)
admin.site.register(models.BeeSpecies)
admin.site.register(models.Ecozone)
admin.site.register(models.StratificationDuration)
admin.site.register(models.NonNativeSpecies)

# ===============
# Register customer and order models
# ===============
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.ShoppingCart)
admin.site.register(models.OrderSeedApplication)
