from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils.translation import override

from project.models import PlantProfile


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
