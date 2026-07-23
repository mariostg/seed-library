import random
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from project import models

DEBUG_CUSTOMER_EMAIL_PREFIX = "debug.customer."
DEBUG_ORDER_NOTE = "Generated for development/debugging."


class Command(BaseCommand):
    help = "Create dummy customer orders for development and debugging."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of orders to create (default: 50).",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=42,
            help="Random seed for reproducible data (default: 42).",
        )
        parser.add_argument(
            "--from-year",
            type=int,
            default=timezone.now().year - 5,
            help="Earliest year for generated orders (default: current year - 5).",
        )
        parser.add_argument(
            "--city",
            type=str,
            help="City for generated orders (default: random).",
        )
        parser.add_argument(
            "--to-year",
            type=int,
            default=timezone.now().year,
            help="Latest year for generated orders (default: current year).",
        )
        parser.add_argument(
            "--clear-existing",
            action="store_true",
            help="Delete existing orders, order items, customers, and carts first.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("This command is only available when DEBUG=True.")

        count = options["count"]
        seed = options["seed"]
        from_year = options["from_year"]
        to_year = options["to_year"]
        city = options["city"]
        clear_existing = options["clear_existing"]

        if count <= 0:
            raise CommandError("--count must be greater than 0")
        if from_year > to_year:
            raise CommandError("--from-year must be less than or equal to --to-year")

        rng = random.Random(seed)

        if clear_existing:
            self.stdout.write(
                "Clearing existing carts, orders, items, and customers..."
            )
            models.ShoppingCart.objects.all().delete()
            models.OrderItem.objects.all().delete()
            models.Order.objects.all().delete()
            models.Customer.objects.all().delete()

        applications = self._ensure_applications()
        plants = self._ensure_plants(rng)

        first_names = [
            "Alex",
            "Marie",
            "Sophie",
            "Liam",
            "Noah",
            "Emma",
            "Olivia",
            "Ethan",
            "Lucas",
            "Camille",
        ]
        last_names = [
            "Martin",
            "Tremblay",
            "Roy",
            "Gagnon",
            "Lee",
            "Wilson",
            "Bouchard",
            "Nguyen",
            "Smith",
            "Brown",
        ]
        ontario_cities = ["Ottawa", "Toronto", "Kingston", "Hamilton", "London"]
        quebec_cities = ["Montreal", "Quebec City", "Gatineau", "Sherbrooke", "Laval"]
        order_statuses = [status for status, _ in models.Order.ORDER_STATUS_CHOICES]

        created_orders = 0
        created_items = 0

        for idx in range(count):
            province = "Ontario" if idx % 2 == 0 else "Quebec"
            if not city:
                city = rng.choice(
                    ontario_cities if province == "Ontario" else quebec_cities
                )

            customer = models.Customer.objects.create(
                first_name=rng.choice(first_names),
                last_name=rng.choice(last_names),
                email=f"{DEBUG_CUSTOMER_EMAIL_PREFIX}{idx + 1}@example.org",
                address=f"{100 + idx} Debug Avenue",
                city=city,
                province=province,
                postal_code=self._postal_code(rng, province),
                application=rng.choice(applications),
            )

            order = models.Order.objects.create(
                customer=customer,
                status=rng.choice(order_statuses),
                donation_amount=rng.choice([0, 0, 0, 5, 10, 20]),
                customer_note=DEBUG_ORDER_NOTE,
            )

            order_dt = self._random_datetime_for_year_range(rng, from_year, to_year)
            models.Order.objects.filter(pk=order.pk).update(
                order_date=order_dt,
                created=order_dt,
                modified=order_dt,
            )

            item_count = rng.randint(1, min(4, len(plants)))
            for plant in rng.sample(plants, item_count):
                models.OrderItem.objects.create(
                    order=order,
                    plant_profile=plant,
                    quantity=rng.randint(1, 5),
                )
                created_items += 1

            created_orders += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created_orders} dummy orders and {created_items} order items."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Date range: {from_year}-{to_year}; provinces: Ontario/Quebec; seed={seed}."
            )
        )

    def _ensure_applications(self):
        defaults = [
            ("Home garden", 3),
            ("School project", 2),
            ("Community restoration", 1),
            ("Pollinator habitat", 2),
        ]
        apps = []
        for name, priority in defaults:
            app, _ = models.OrderSeedApplication.objects.get_or_create(
                seed_application=name,
                defaults={"priority": priority},
            )
            apps.append(app)
        return apps

    def _ensure_plants(self, rng):
        plants = list(models.PlantProfile.all_objects.order_by("pk")[:30])
        if len(plants) >= 10:
            return plants

        # Ensure enough plants exist so order items can vary in debugging scenarios.
        missing = 10 - len(plants)
        for i in range(missing):
            latin_name = f"Debugplant {rng.randint(1000, 9999)} {i}"
            plant = models.PlantProfile.all_objects.create(
                latin_name=latin_name,
                english_name=f"Debug Plant {i}",
                french_name=f"Plante test {i}",
                is_active=True,
                is_accepted=True,
                is_draft=False,
            )
            plants.append(plant)
        return plants

    def _postal_code(self, rng, province):
        letters = "ABCEGHJKLMNPRSTVXY"
        if province == "Quebec":
            first = "G"
        else:
            first = "K"
        return (
            f"{first}{rng.choice(letters)}{rng.randint(0, 9)} "
            f"{rng.randint(0, 9)}{rng.choice(letters)}{rng.randint(0, 9)}"
        )

    def _random_datetime_for_year_range(self, rng, from_year, to_year):
        year = rng.randint(from_year, to_year)
        start = datetime(year, 1, 1, 8, 0, 0)
        end = datetime(year, 12, 31, 20, 0, 0)
        delta_seconds = int((end - start).total_seconds())
        return timezone.make_aware(
            start + timedelta(seconds=rng.randint(0, delta_seconds))
        )
