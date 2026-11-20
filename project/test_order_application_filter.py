from unittest.mock import patch

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import override

from project.models import Customer, Order, OrderSeedApplication, ProjectUser
from project.tasks import _build_filtered_orders_queryset


class OrderApplicationFilterTests(TestCase):
    def setUp(self):
        manager = ProjectUser.objects.create_user(username="application-manager")
        group, _ = Group.objects.get_or_create(name="Shop Manager")
        manager.groups.add(group)
        self.client.force_login(manager)
        garden = OrderSeedApplication.objects.create(seed_application="Personal Garden")
        self.garden = garden
        school = OrderSeedApplication.objects.create(seed_application="School Project")
        garden_customer = Customer.objects.create(
            first_name="Garden",
            last_name="Customer",
            email="garden@example.com",
            address="1 Main St",
            city="Ottawa",
            province="ON",
            postal_code="A1A 1A1",
            application=garden,
        )
        school_customer = Customer.objects.create(
            first_name="School",
            last_name="Customer",
            email="school@example.com",
            address="2 Main St",
            city="Ottawa",
            province="ON",
            postal_code="B2B 2B2",
            application=school,
        )
        self.garden_order = Order.objects.create(customer=garden_customer)
        self.school_order = Order.objects.create(customer=school_customer)
        with override("en"):
            self.url = reverse("admin-order-management-page")
            self.pdf_url = reverse("admin-order-filtered-to-pdf")

    def test_application_filter_and_choices(self):
        response = self.client.get(self.url, {"order_seed_application": self.garden.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["page_obj"]), [self.garden_order])
        self.assertContains(response, 'name="order_seed_application"')
        self.assertContains(response, "<select")
        self.assertContains(response, f'value="{self.garden.pk}" selected')
        self.assertContains(response, "Personal Garden")
        self.assertContains(response, "School Project")
        self.assertIn(
            f"order_seed_application={self.garden.pk}", response.context["query_string"]
        )

    def test_blank_filter(self):
        response = self.client.get(self.url, {"order_seed_application": ""})
        self.assertCountEqual(
            response.context["page_obj"], [self.garden_order, self.school_order]
        )

    def test_filter_combines_with_status(self):
        response = self.client.get(
            self.url, {"order_seed_application": self.garden.pk, "status": "completed"}
        )
        self.assertEqual(list(response.context["page_obj"]), [])

    def test_selects_application_by_id_not_matching_text(self):
        other = OrderSeedApplication.objects.create(seed_application="Personal Garden")
        self.school_order.customer.application = other
        self.school_order.customer.save(update_fields=["application"])
        response = self.client.get(self.url, {"order_seed_application": self.garden.pk})
        self.assertEqual(list(response.context["page_obj"]), [self.garden_order])

    def test_french_filter_labels(self):
        with override("fr"):
            url = reverse("admin-order-management-page")
            response = self.client.get(url)
        self.assertContains(response, "Toutes les utilisations")

    @patch("project.views.generate_filtered_orders_pdf_task.delay")
    def test_invalid_application_never_returns_or_queues_unfiltered_orders(self, delay):
        for value in ("invalid", "999999"):
            with self.subTest(value=value):
                params = {"order_seed_application": value}
                self.assertEqual(self.client.get(self.url, params).status_code, 400)
                self.assertEqual(self.client.get(self.pdf_url, params).status_code, 400)
                with self.assertRaisesRegex(
                    ValueError, "Invalid order seed application"
                ):
                    _build_filtered_orders_queryset(params)
        delay.assert_not_called()

    @patch("project.views.generate_filtered_orders_pdf_task.delay")
    def test_pdf_receives_and_applies_application_filter(self, delay):
        delay.return_value.id = "application-filter-task"
        response = self.client.get(
            self.pdf_url, {"order_seed_application": self.garden.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            delay.call_args.kwargs["filter_params"],
            {"order_seed_application": str(self.garden.pk)},
        )
        self.assertEqual(
            list(
                _build_filtered_orders_queryset(
                    {"order_seed_application": str(self.garden.pk)}
                )
            ),
            [self.garden_order],
        )
