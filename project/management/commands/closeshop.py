# a command to close the shop which prevents customer to place items in the cart
from django.core.management.base import BaseCommand

from project.models import LibrarySetting


class Command(BaseCommand):
    """
    Close the shop management command.

    Checks for a LibrarySetting identified by "is_shop_open" (creating it if necessary)
    and sets its `is_shop_open` attribute to False to prevent customers from placing
    items in the cart.

    Usage:
        python manage.py closeshop

    Behavior:
    - If the setting does not exist, it is created.
    - If `is_shop_open` is already False, a warning is written and no change is made.
    - If `is_shop_open` is True, it is set to False, saved, and a success message is written.

    Side effects:
    - Persists the LibrarySetting change to the database.

    Assumptions:
    - LibrarySetting.objects.get_or_create("is_shop_open") returns an object with an
      `is_shop_open` boolean attribute and a `save()` method.
    - Command inherits from Django's BaseCommand and can use self.stdout and self.style.
    """

    help = "Closes the shop to prevent customers from placing items in the cart"

    def handle(self, *args, **kwargs):
        setting, created = LibrarySetting.objects.get_or_create("is_shop_open")
        if not setting.is_shop_open:
            self.stdout.write(self.style.WARNING("Shop is already closed."))
            return
        setting.is_shop_open = False
        setting.save()
        self.stdout.write(self.style.SUCCESS("Shop has been closed successfully."))
