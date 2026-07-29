import io
from datetime import datetime
from unittest.mock import patch

from django.contrib import messages as django_messages
from django.contrib.auth.models import Group
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import override

from project.models import (
    Customer,
    Order,
    OrderSeedApplication,
    PlantNarrative,
    PlantProfile,
    ProjectUser,
)


class SearchPlantNameTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.plant1 = PlantProfile.objects.create(
            latin_name="Abies balsamea", seed_availability=True
        )
        self.plant2 = PlantProfile.objects.create(latin_name="Betula papyrifera")
        self.search_url = reverse("search-plant-name")

    def test_empty_search_returns_no_results(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)
        self.assertTemplateUsed(response, "project/plant-catalog.html")

    def test_search_returns_correct_plant(self):
        response = self.client.get(
            self.search_url + "?seed_availability=available-seed"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        plant = response.context["object_list"][0]
        self.assertEqual(plant.latin_name, "Abies balsamea")

    def test_search_returns_all_plants_ordered(self):
        response = self.client.get(self.search_url + "?any_name=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 2)
        plants = list(response.context["object_list"])
        self.assertEqual(plants[0].latin_name, "Abies balsamea")
        self.assertEqual(plants[1].latin_name, "Betula papyrifera")

    def test_htmx_request_uses_different_template(self):
        response = self.client.get(self.search_url, headers={"hx-request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/plant-search-results.html")

    def test_context_contains_required_data(self):
        response = self.client.get(self.search_url)
        self.assertIn("search_filter", response.context)
        self.assertIn("object_list", response.context)
        self.assertEqual(response.context["url_name"], "index")
        self.assertEqual(response.context["title"], "Plant Profile Filter")


class DonationViewsTest(TestCase):
    def setUp(self):
        self.client = Client(headers={"host": "localhost"})
        with override("en"):
            self.donation_page_url = reverse("donation-page")
            self.checkout_url = reverse("donation-checkout-session")

    def test_donation_page_loads(self):
        response = self.client.get(self.donation_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/donations.html")

    @override_settings(
        STRIPE_SECRET_KEY="sk_test_key",
        STRIPE_PUBLISHABLE_KEY="pk_test_key",
        STRIPE_DONATION_MIN_AMOUNT="1.00",
    )
    @patch("project.views.stripe")
    def test_create_checkout_session_one_time(self, mock_stripe):
        mock_stripe.checkout.Session.create.return_value.url = (
            "https://checkout.stripe.com/test-session"
        )

        response = self.client.post(
            self.checkout_url,
            data={"donation_amount": "25.00"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://checkout.stripe.com/test-session")
        call_kwargs = mock_stripe.checkout.Session.create.call_args.kwargs
        self.assertEqual(call_kwargs["mode"], "payment")
        self.assertEqual(
            call_kwargs["line_items"][0]["price_data"]["unit_amount"], 2500
        )

    @override_settings(
        STRIPE_SECRET_KEY="sk_test_key",
        STRIPE_PUBLISHABLE_KEY="pk_test_key",
        STRIPE_DONATION_MIN_AMOUNT="1.00",
    )
    @patch("project.views.stripe")
    def test_create_checkout_session_recurring(self, mock_stripe):
        mock_stripe.checkout.Session.create.return_value.url = (
            "https://checkout.stripe.com/test-subscription"
        )

        response = self.client.post(
            self.checkout_url,
            data={"donation_amount": "12.50", "is_recurring": "on"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://checkout.stripe.com/test-subscription")
        call_kwargs = mock_stripe.checkout.Session.create.call_args.kwargs
        self.assertEqual(call_kwargs["mode"], "subscription")
        self.assertEqual(
            call_kwargs["line_items"][0]["price_data"]["recurring"]["interval"],
            "month",
        )

    @override_settings(
        STRIPE_SECRET_KEY="sk_test_key",
        STRIPE_PUBLISHABLE_KEY="pk_test_key",
        STRIPE_DONATION_MIN_AMOUNT="5.00",
    )
    @patch("project.views.stripe")
    def test_create_checkout_session_rejects_small_amount(self, mock_stripe):
        response = self.client.post(
            self.checkout_url,
            data={"donation_amount": "2.00"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/donations.html")
        mock_stripe.checkout.Session.create.assert_not_called()


class PlantProfilePageContextTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.plant = PlantProfile.objects.create(latin_name="Abies balsamea")
        self.narrative = PlantNarrative.objects.create(
            plant_profile=self.plant,
            description="Narrative for profile page context test.",
            published=True,
        )
        self.url = reverse("plant-profile-page", kwargs={"pk": self.plant.pk})

    def test_context_contains_plant_narratives(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("plant_narratives", response.context)
        narratives = response.context["plant_narratives"]
        self.assertIn(self.narrative, narratives)


class AdminOrderManagementFilterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = ProjectUser.objects.create_user(
            username="order-manager",
            password="test-pass-123",
        )
        library_manager_group, _ = Group.objects.get_or_create(name="Library Manager")
        self.user.groups.add(library_manager_group)
        self.client.force_login(self.user)

        self.application = OrderSeedApplication.objects.create(
            seed_application="Personal Garden"
        )

        self.customer_one = Customer.objects.create(
            first_name="John",
            last_name="Smith",
            email="john@example.com",
            address="1 Main St",
            city="Ottawa",
            province="ON",
            postal_code="A1A1A1",
            application=self.application,
        )
        self.customer_two = Customer.objects.create(
            first_name="Alice",
            last_name="Brown",
            email="alice@example.com",
            address="2 Main St",
            city="Ottawa",
            province="ON",
            postal_code="B2B2B2",
            application=self.application,
        )

        self.order_pending = Order.objects.create(
            customer=self.customer_one,
            status="pending",
        )
        self.order_completed = Order.objects.create(
            customer=self.customer_two,
            status="completed",
        )

        Order.objects.filter(pk=self.order_pending.pk).update(
            order_date=timezone.make_aware(datetime(2025, 6, 1, 12, 0, 0))
        )
        Order.objects.filter(pk=self.order_completed.pk).update(
            order_date=timezone.make_aware(datetime(2024, 6, 1, 12, 0, 0))
        )

        self.order_pending.refresh_from_db()
        self.order_completed.refresh_from_db()

    def test_order_management_renders_filter_form(self):
        with override("en"):
            url = reverse("admin-order-management-page")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="status"')
        self.assertContains(response, 'name="order_year"')
        self.assertContains(response, 'name="customer_first_name"')
        self.assertContains(response, 'name="customer_last_name"')

    def test_filter_by_status(self):
        with override("en"):
            url = reverse("admin-order-management-page")

        response = self.client.get(url, {"status": "completed"})

        self.assertEqual(response.status_code, 200)
        orders = list(response.context["page_obj"].object_list)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.order_completed.id)

    def test_filter_by_order_year(self):
        with override("en"):
            url = reverse("admin-order-management-page")

        response = self.client.get(url, {"order_year": "2025"})

        self.assertEqual(response.status_code, 200)
        orders = list(response.context["page_obj"].object_list)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.order_pending.id)

    def test_filter_by_customer_name(self):
        with override("en"):
            url = reverse("admin-order-management-page")

        response = self.client.get(url, {"customer_last_name": "bro"})

        self.assertEqual(response.status_code, 200)
        orders = list(response.context["page_obj"].object_list)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.order_completed.id)

    @patch("project.views.generate_filtered_orders_pdf_task.delay")
    def test_filtered_pdf_enqueue_uses_active_filters(self, mock_delay):
        mock_delay.return_value.id = "task-filtered-123"
        with override("en"):
            enqueue_url = reverse("admin-order-filtered-to-pdf")
            download_url = reverse(
                "admin-order-filtered-pdf-download",
                kwargs={"task_id": "task-filtered-123"},
            )

        response = self.client.get(enqueue_url, {"status": "completed"}, follow=True)

        self.assertEqual(response.status_code, 200)
        mock_delay.assert_called_once_with(
            filter_params={"status": "completed"},
            generated_by_user_id=self.user.id,
        )

        messages = [str(message) for message in response.context["messages"]]
        self.assertTrue(
            any(
                "Filtered-orders PDF generation started." in message
                for message in messages
            )
        )
        self.assertTrue(any(download_url in message for message in messages))


class AdminFilteredOrdersPdfAsyncTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = ProjectUser.objects.create_user(
            username="filtered-manager",
            password="test-pass-123",
        )
        library_manager_group, _ = Group.objects.get_or_create(name="Library Manager")
        self.user.groups.add(library_manager_group)
        self.client.force_login(self.user)

    @patch("project.views.AsyncResult")
    def test_filtered_pdf_download_not_ready_redirects_with_message(
        self,
        mock_async_result,
    ):
        mock_async_result.return_value.ready.return_value = False
        with override("en"):
            download_url = reverse(
                "admin-order-filtered-pdf-download", kwargs={"task_id": "task-123"}
            )
            order_management_url = reverse("admin-order-management-page")

        response = self.client.get(download_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, order_management_url)

        messages = [
            str(message)
            for message in django_messages.get_messages(response.wsgi_request)
        ]
        self.assertTrue(
            any(
                "Filtered-orders PDF is still generating." in message
                for message in messages
            )
        )

    @patch("project.views.default_storage.open")
    @patch("project.views.default_storage.exists")
    @patch("project.views.AsyncResult")
    def test_filtered_pdf_download_ready_returns_pdf_response(
        self,
        mock_async_result,
        mock_exists,
        mock_open,
    ):
        mock_task = mock_async_result.return_value
        mock_task.ready.return_value = True
        mock_task.failed.return_value = False
        mock_task.result = "generated/filtered-orders/filtered_orders_task-123.pdf"
        mock_exists.return_value = True
        mock_open.return_value = io.BytesIO(b"%PDF-1.4\n")
        with override("en"):
            download_url = reverse(
                "admin-order-filtered-pdf-download", kwargs={"task_id": "task-123"}
            )

        response = self.client.get(download_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("Filtered_Orders.pdf", response["Content-Disposition"])
