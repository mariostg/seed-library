from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from project.models import (
    Customer,
    Order,
    OrderItem,
    OrderSeedApplication,
    PlantProfile,
    StratificationDuration,
)


class AnalyzePlantProfilesCommandTest(TestCase):
    def test_reports_double_dormancy_without_stratification(self):
        PlantProfile.objects.create(
            latin_name="Invalid Plant",
            double_dormancy=True,
            inaturalist_taxon="12345",
        )
        duration = StratificationDuration.objects.create(stratification_duration=90)
        PlantProfile.objects.create(
            latin_name="Valid Plant",
            double_dormancy=True,
            stratification_duration=duration,
            inaturalist_taxon="67890",
        )

        stdout = StringIO()

        call_command(
            "analyze_plant_profiles",
            "--check",
            "double_dormancy_requires_stratification",
            stdout=stdout,
        )

        output = stdout.getvalue()
        self.assertIn("double_dormancy_requires_stratification", output)
        self.assertIn("Invalid plant", output)
        self.assertNotIn("Valid plant", output)
        self.assertIn("1 issue(s) found", output)

    def test_fail_on_issues_raises_command_error(self):
        PlantProfile.objects.create(
            latin_name="Invalid Plant",
            double_dormancy=True,
            inaturalist_taxon="12345",
        )

        with self.assertRaisesMessage(CommandError, "1 issue(s) found"):
            call_command(
                "analyze_plant_profiles",
                "--check",
                "double_dormancy_requires_stratification",
                "--fail-on-issues",
            )

    def test_reports_missing_inaturalist_taxon(self):
        PlantProfile.objects.create(
            latin_name="Missing Taxon",
            inaturalist_taxon="",
        )
        PlantProfile.objects.create(
            latin_name="Has Taxon",
            inaturalist_taxon="12345",
        )

        stdout = StringIO()

        call_command(
            "analyze_plant_profiles",
            "--check",
            "missing_inaturalist_taxon",
            stdout=stdout,
        )

        output = stdout.getvalue()
        self.assertIn("missing_inaturalist_taxon", output)
        self.assertIn("Missing taxon", output)
        self.assertNotIn("Has taxon", output)
        self.assertIn("1 issue(s) found", output)

    def test_reports_missing_taxon(self):
        PlantProfile.objects.create(
            latin_name="Missing Vascan Taxon",
            taxon="",
            inaturalist_taxon="12345",
        )
        PlantProfile.objects.create(
            latin_name="Has Vascan Taxon",
            taxon="54321",
            inaturalist_taxon="67890",
        )

        stdout = StringIO()

        call_command(
            "analyze_plant_profiles",
            "--check",
            "missing_taxon",
            stdout=stdout,
        )

        output = stdout.getvalue()
        self.assertIn("missing_taxon", output)
        self.assertIn("Missing vascan taxon", output)
        self.assertNotIn("Has vascan taxon", output)
        self.assertIn("1 issue(s) found", output)


class CreateDummyOrdersCommandTest(TestCase):
    @override_settings(DEBUG=True)
    def test_creates_orders_with_on_qc_and_varied_years(self):
        for i in range(12):
            PlantProfile.objects.create(
                latin_name=f"Debug Seed Plant {i}",
                inaturalist_taxon=str(10000 + i),
            )

        call_command(
            "create_dummy_orders",
            "--count",
            "50",
            "--seed",
            "777",
            "--from-year",
            "2021",
            "--to-year",
            "2026",
        )

        self.assertEqual(Order.objects.count(), 50)
        self.assertGreater(OrderItem.objects.count(), 0)

        provinces = set(Customer.objects.values_list("province", flat=True))
        self.assertIn("Ontario", provinces)
        self.assertIn("Quebec", provinces)

        years = set(Order.objects.values_list("order_date__year", flat=True).distinct())
        self.assertGreaterEqual(len(years), 3)


class DeleteDebugOrdersCommandTest(TestCase):
    @override_settings(DEBUG=True)
    def test_dry_run_does_not_delete_data(self):
        for i in range(10):
            PlantProfile.objects.create(
                latin_name=f"Dry Run Plant {i}",
                inaturalist_taxon=str(20000 + i),
            )

        call_command("create_dummy_orders", "--count", "8", "--seed", "5")
        before = Order.objects.count()

        call_command("delete_debug_orders", "--dry-run")

        self.assertEqual(Order.objects.count(), before)

    @override_settings(DEBUG=True)
    def test_deletes_only_debug_generated_orders(self):
        for i in range(10):
            PlantProfile.objects.create(
                latin_name=f"Delete Debug Plant {i}",
                inaturalist_taxon=str(30000 + i),
            )

        call_command("create_dummy_orders", "--count", "6", "--seed", "9")

        app = OrderSeedApplication.objects.create(
            seed_application="Real user application",
            priority=5,
        )
        real_customer = Customer.objects.create(
            first_name="Real",
            last_name="User",
            email="real.user@example.org",
            address="1 Main Street",
            city="Ottawa",
            province="Ontario",
            postal_code="K1A 0A1",
            application=app,
        )
        real_order = Order.objects.create(
            customer=real_customer,
            status="pending",
            customer_note="Real order - keep me",
        )
        OrderItem.objects.create(
            order=real_order,
            plant_profile=PlantProfile.objects.first(),
            quantity=2,
        )

        call_command("delete_debug_orders", "--delete-debug-customers")

        self.assertEqual(Order.objects.filter(id=real_order.id).count(), 1)
        self.assertEqual(Customer.objects.filter(id=real_customer.id).count(), 1)
        self.assertEqual(
            Order.objects.exclude(id=real_order.id).count(),
            0,
        )


class ValidateEncryptedEmailsCommandTest(TestCase):
    def setUp(self):
        self.application = OrderSeedApplication.objects.create(
            seed_application="Validation test application",
            priority=10,
        )

    def test_reports_invalid_customer_token(self):
        customer = Customer.objects.create(
            first_name="Invalid",
            last_name="Customer",
            email="invalid.customer@example.org",
            address="10 Broken Key Street",
            city="Ottawa",
            province="Ontario",
            postal_code="K1A 0A1",
            application=self.application,
        )
        Customer.objects.filter(pk=customer.pk).update(email_encrypted="not-a-token")

        stdout = StringIO()
        call_command("validate_encrypted_emails", "--scope", "customers", stdout=stdout)

        output = stdout.getvalue()
        self.assertIn(
            "[customers] checked 1 encrypted email token(s); invalid token(s): 1",
            output,
        )
        self.assertIn(f"Customer id={customer.pk} has an invalid token", output)

    def test_fail_on_invalid_raises_command_error(self):
        customer = Customer.objects.create(
            first_name="Fail",
            last_name="Case",
            email="fail.case@example.org",
            address="11 Broken Key Street",
            city="Ottawa",
            province="Ontario",
            postal_code="K1A 0A1",
            application=self.application,
        )
        Customer.objects.filter(pk=customer.pk).update(email_encrypted="not-a-token")

        with self.assertRaisesMessage(
            CommandError, "Invalid encrypted email token(s) found: 1"
        ):
            call_command("validate_encrypted_emails", "--fail-on-invalid")

    def test_users_scope_reports_invalid_project_user_token(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="badtokenuser",
            email="badtoken@example.org",
            password="test-pass-123",
        )
        user_model.objects.filter(pk=user.pk).update(email_encrypted="not-a-token")

        stdout = StringIO()
        call_command("validate_encrypted_emails", "--scope", "users", stdout=stdout)

        output = stdout.getvalue()
        self.assertIn(
            "[users] checked 1 encrypted email token(s); invalid token(s): 1", output
        )
        self.assertIn(f"ProjectUser id={user.pk} has an invalid token", output)
