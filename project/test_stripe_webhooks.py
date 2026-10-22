from decimal import Decimal
from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from project import models


class StripeWebhookTest(TestCase):
    def setUp(self):
        self.client = Client(headers={"host": "localhost"})
        self.url = reverse("stripe-webhook")

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.views.stripe")
    @patch("project.views.send_donation_receipt_task.delay")
    def test_checkout_session_completed_creates_donation(
        self, mock_receipt_task, mock_stripe
    ):
        event = {
            "id": "evt_checkout_1",
            "type": "checkout.session.completed",
            "livemode": False,
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "mode": "payment",
                    "currency": "cad",
                    "amount_total": 2500,
                    "payment_intent": "pi_test_123",
                    "subscription": None,
                    "customer": "cus_test_123",
                    "metadata": {"is_recurring": "false", "donation_amount": "25.00"},
                    "customer_details": {
                        "email": "donor@example.com",
                        "name": "Donor Name",
                    },
                }
            },
        }
        mock_stripe.Webhook.construct_event.return_value = event

        response = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.StripeWebhookEvent.objects.count(), 1)
        self.assertEqual(models.Donation.objects.count(), 1)

        donation = models.Donation.objects.first()
        self.assertEqual(donation.stripe_checkout_session_id, "cs_test_123")
        self.assertEqual(str(donation.amount), "25.00")
        self.assertEqual(donation.status, models.Donation.STATUS_SUCCEEDED)
        self.assertFalse(donation.is_recurring)
        mock_receipt_task.assert_called_once_with(donation.id)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.views.stripe")
    @patch("project.views.send_donation_receipt_task.delay")
    def test_subscription_checkout_completed_sends_receipt(
        self, mock_receipt_task, mock_stripe
    ):
        event = {
            "id": "evt_subscription_checkout",
            "type": "checkout.session.completed",
            "livemode": False,
            "data": {
                "object": {
                    "id": "cs_test_subscription",
                    "mode": "subscription",
                    "currency": "cad",
                    "amount_total": 2500,
                    "payment_intent": "pi_test_subscription",
                    "subscription": "sub_test_subscription",
                    "customer": "cus_test_subscription",
                    "metadata": {"is_recurring": "true"},
                    "customer_details": {
                        "email": "subscriber@example.com",
                        "name": "Subscriber",
                    },
                }
            },
        }
        mock_stripe.Webhook.construct_event.return_value = event

        response = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )

        self.assertEqual(response.status_code, 200)
        donation = models.Donation.objects.get(
            stripe_checkout_session_id="cs_test_subscription"
        )
        self.assertTrue(donation.is_recurring)
        mock_receipt_task.assert_called_once_with(donation.id)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.views.stripe")
    @patch("project.views.send_donation_receipt_task.delay")
    def test_duplicate_event_is_idempotent(self, mock_receipt_task, mock_stripe):
        event = {
            "id": "evt_dup_1",
            "type": "checkout.session.completed",
            "livemode": False,
            "data": {
                "object": {
                    "id": "cs_test_dup",
                    "mode": "payment",
                    "currency": "cad",
                    "amount_total": 1000,
                    "customer": "cus_test_dup",
                    "metadata": {"is_recurring": "false"},
                    "customer_details": {"email": "dup@example.com", "name": "Dup"},
                }
            },
        }
        mock_stripe.Webhook.construct_event.return_value = event

        response1 = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )
        response2 = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(models.StripeWebhookEvent.objects.count(), 1)
        self.assertEqual(models.Donation.objects.count(), 1)
        mock_receipt_task.assert_called_once()

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.views.stripe")
    def test_invoice_paid_creates_recurring_donation(self, mock_stripe):
        event = {
            "id": "evt_invoice_1",
            "type": "invoice.paid",
            "livemode": False,
            "data": {
                "object": {
                    "id": "in_test_123",
                    "subscription": "sub_test_123",
                    "customer": "cus_test_123",
                    "payment_intent": "pi_test_123",
                    "currency": "cad",
                    "amount_paid": 3200,
                    "billing_reason": "subscription_cycle",
                }
            },
        }
        mock_stripe.Webhook.construct_event.return_value = event

        response = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )

        self.assertEqual(response.status_code, 200)
        donation = models.Donation.objects.get(stripe_invoice_id="in_test_123")
        self.assertEqual(str(donation.amount), "32.00")
        self.assertEqual(donation.status, models.Donation.STATUS_SUCCEEDED)
        self.assertTrue(donation.is_recurring)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.views.stripe")
    def test_stripe_object_with_decimal_payload_is_serializable(self, mock_stripe):
        event = {
            "id": "evt_invoice_decimal",
            "type": "invoice.paid",
            "livemode": False,
            "data": {
                "object": {
                    "id": "in_test_decimal",
                    "subscription": "sub_test_decimal",
                    "currency": "cad",
                    "amount_paid": 3200,
                    "lines": {
                        "data": [{"pricing": {"unit_amount_decimal": Decimal("32.00")}}]
                    },
                }
            },
        }
        mock_stripe.Webhook.construct_event.return_value = event

        response = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            models.StripeWebhookEvent.objects.filter(
                stripe_event_id="evt_invoice_decimal"
            ).exists()
        )

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.views.stripe")
    def test_invalid_signature_returns_400(self, mock_stripe):
        mock_stripe.Webhook.construct_event.side_effect = ValueError("bad signature")

        response = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            headers={"stripe-signature": "sig_test"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.StripeWebhookEvent.objects.count(), 0)
        self.assertEqual(models.Donation.objects.count(), 0)
