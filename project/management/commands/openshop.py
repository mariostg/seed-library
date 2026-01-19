# a command to open the shop which allows customers to place items in the cart

from django.core.management.base import BaseCommand

from project.models import LibrarySetting


class Command(BaseCommand):
    """Management command to open the shop.

    This Django management command ensures the 'is_shop_open' library setting exists and sets it to True
    so customers can place items in the cart. Behavior:
    - Retrieves or creates the LibrarySetting for the "is_shop_open" key.
    - If the setting already indicates the shop is open, writes a warning and exits without making changes.
    - Otherwise sets is_shop_open to True, saves the setting, and writes a success message.

    Side effects:
    - May create a LibrarySetting record.
    - Updates and saves the LibrarySetting to the database.

    Notes:
    - The command is idempotent: running it when the shop is already open has no effect.
    - Database errors or other exceptions raised by the ORM will propagate.
    """

    help = "Opens the shop to allow customers to place items in the cart"

    def handle(self, *args, **kwargs):
        setting, created = LibrarySetting.objects.get_or_create("is_shop_open")
        if setting.is_shop_open:
            self.stdout.write(self.style.WARNING("Shop is already open."))
            return
        setting.is_shop_open = True
        setting.save()
        self.stdout.write(self.style.SUCCESS("Shop has been opened successfully."))
