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
    @patch("project.tasks.send_donation_thank_you_task.delay")
    @patch("project.views.stripe")
    def test_paid_checkout_donation_updates_linked_order(
        self, mock_stripe, mock_thank_you_task
    ):
        customer = models.Customer.objects.create(
            first_name="Jamie",
            last_name="Donor",
            email="jamie@example.com",
            address="12 Garden Road",
            city="Ottawa",
            province="Ontario",
            postal_code="K1A 0B1",
        )
        order = models.Order.objects.create(customer=customer)
        donation = models.Donation.objects.create(
            order=order,
            amount=Decimal("15.00"),
            status=models.Donation.STATUS_PENDING,
        )
        event = {
            "id": "evt_order_donation",
            "type": "checkout.session.completed",
            "livemode": False,
            "data": {
                "object": {
                    "id": "cs_order_donation",
                    "mode": "payment",
                    "payment_status": "paid",
                    "currency": "cad",
                    "amount_total": 1500,
                    "payment_intent": "pi_order_donation",
                    "metadata": {
                        "donation_id": str(donation.id),
                        "order_id": str(order.id),
                    },
                    "customer_details": {
                        "email": "jamie@example.com",
                        "name": "Jamie Donor",
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
        donation.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(donation.status, models.Donation.STATUS_SUCCEEDED)
        self.assertEqual(donation.donor_name, "Jamie Donor")
        self.assertEqual(donation.donor_email, "jamie@example.com")
        self.assertIn("12 Garden Road", donation.donor_address)
        self.assertEqual(order.donation_amount, Decimal("15.00"))
        mock_thank_you_task.assert_called_once_with(order.id)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    @patch("project.tasks.send_donation_thank_you_task.delay")
    @patch("project.views.stripe")
    def test_unpaid_checkout_donation_does_not_update_order_or_send_thanks(
        self, mock_stripe, mock_thank_you_task
    ):
        customer = models.Customer.objects.create(
            first_name="Taylor",
            last_name="Donor",
            email="taylor@example.com",
            address="3 Seed Lane",
            city="Ottawa",
            province="Ontario",
            postal_code="K1A 0B1",
        )
        order = models.Order.objects.create(customer=customer)
        donation = models.Donation.objects.create(
            order=order,
            amount=Decimal("20.00"),
            status=models.Donation.STATUS_PENDING,
            stripe_checkout_session_id="cs_order_unpaid",
        )
        event = {
            "id": "evt_order_donation_unpaid",
            "type": "checkout.session.completed",
            "livemode": False,
            "data": {
                "object": {
                    "id": "cs_order_unpaid",
                    "mode": "payment",
                    "payment_status": "unpaid",
                    "currency": "cad",
                    "amount_total": 2000,
                    "metadata": {
                        "donation_id": str(donation.id),
                        "order_id": str(order.id),
                    },
                    "customer_details": {
                        "email": "taylor@example.com",
                        "name": "Taylor Donor",
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
        donation.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(donation.status, models.Donation.STATUS_PENDING)
        self.assertEqual(order.donation_amount, Decimal("0.00"))
        mock_thank_you_task.assert_not_called()

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
