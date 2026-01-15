# a Middleware class to to check library settings on each request

from django.db import models

from project.models import LibrarySetting, ShoppingCart


class LibrarySettingsMiddleware:
    """
    Middleware to attach library settings to each request object.
    This allows easy access to library-specific settings throughout the application.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Attach library settings to the request object
        request.library_settings = self.get_library_settings()
        customer_id = request.session.get("customer_id")
        if request.library_settings.is_shop_open and customer_id:
            request.cart_item_count = self.get_cart_item_count(customer_id)
        response = self.get_response(request)
        return response

    def get_cart_item_count(self, customer_id):
        item_count = ShoppingCart.objects.filter(customer__id=customer_id).aggregate(
            total_quantity=models.Sum("quantity")
        )["total_quantity"]
        if not item_count:
            item_count = 0
        return item_count

    def get_library_settings(self):
        # Fetch library settings from the database
        try:
            settings = LibrarySetting.objects.first()
            if not settings:
                settings = LibrarySetting.objects.create()
            return settings
        except LibrarySetting.DoesNotExist:
            return LibrarySetting.objects.create()
