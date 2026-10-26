import csv
import io
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone, translation

from project.models import Donation, ProjectUser


class DonationReportTests(TestCase):
    def setUp(self):
        user = ProjectUser.objects.create_user(
            username="donation-manager",
            password="test-password",
            email="manager@example.com",
        )
        shop_manager, _ = Group.objects.get_or_create(name="Shop Manager")
        user.groups.add(shop_manager)
        self.client.force_login(user)

        self.paid_donation = Donation.objects.create(
            amount=Decimal("25.00"),
            currency="cad",
            status=Donation.STATUS_SUCCEEDED,
            donor_name="Casey Gardener",
            donor_email="casey@example.com",
            donor_address="4 Garden Street, Ottawa, Ontario, K1A 0B1",
            paid_at=timezone.now(),
        )
        Donation.objects.create(
            amount=Decimal("10.00"),
            currency="cad",
            status=Donation.STATUS_PENDING,
            donor_name="Pending Donor",
            donor_email="pending@example.com",
            paid_at=timezone.now() + timedelta(days=1),
        )
        with translation.override("en"):
            self.report_url = reverse("admin-donation-report")
            self.csv_url = reverse("admin-donation-report-csv")

    def test_html_report_lists_only_paid_donations(self):
        response = self.client.get(self.report_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Casey Gardener")
        self.assertContains(response, "casey@example.com")
        self.assertContains(response, "4 Garden Street")
        self.assertNotContains(response, "Pending Donor")

    def test_csv_export_contains_requested_donor_fields(self):
        response = self.client.get(self.csv_url)

        self.assertEqual(response.status_code, 200)
        rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
        self.assertEqual(
            rows[0],
            ["Full name", "Donation amount", "Address", "Email", "Donation date"],
        )
        self.assertEqual(rows[1][0], "Casey Gardener")
        self.assertEqual(rows[1][1], "25.00")
        self.assertEqual(rows[1][3], "casey@example.com")
        self.assertEqual(len(rows), 2)

    def test_report_date_filter_is_passed_through_to_csv_link(self):
        today = timezone.localdate().isoformat()

        response = self.client.get(
            self.report_url, {"date_from": today, "date_to": today}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"date_from={today}")
        self.assertContains(response, f"date_to={today}")
