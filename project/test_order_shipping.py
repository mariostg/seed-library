from unittest.mock import patch

from django.contrib.auth.models import Group
from django.core import mail
from django.db import transaction
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils.translation import override
from kombu.exceptions import OperationalError

from project.models import Customer, Order, OrderItem, PlantProfile, ProjectUser
from project.tasks import send_order_shipped_task
from project.utils import (
    get_order_statistics,
    send_order_confirmation_email,
    send_order_shipped_email,
)
from project.views import _build_order_scan_import_preview


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class OrderShippingTests(TestCase):
    def setUp(self):
        manager = ProjectUser.objects.create_user(username="shipping-manager")
        group, _ = Group.objects.get_or_create(name="Shop Manager")
        manager.groups.add(group)
        self.client.force_login(manager)
        self.customer = Customer.objects.create(
            first_name="Ada",
            last_name="Gardener",
            email="ada@example.com",
            address="123 Garden Road",
            city="Ottawa",
            province="ON",
            postal_code="K1A 0B1",
        )
        self.order = Order.objects.create(customer=self.customer, status="completed")
        plant = PlantProfile.objects.create(
            latin_name="Asclepias tuberosa", english_name="Butterfly Milkweed"
        )
        OrderItem.objects.create(order=self.order, plant_profile=plant, quantity=2)
        with override("en"):
            self.url = reverse("admin-order-confirm-shipped", args=[self.order.pk])
            self.management_url = reverse("admin-order-management-page")

    @patch("project.views.send_order_shipped_task.delay")
    def test_completed_order_is_shipped_and_queued_after_commit(self, delay):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.url)
            delay.assert_not_called()
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "shipped")
        delay.assert_called_once_with(self.order.pk)
        self.assertRedirects(
            response, self.management_url, fetch_redirect_response=False
        )
        messages = [str(message) for message in response.wsgi_request._messages]
        self.assertTrue(any("queued" in message for message in messages))

    @patch("project.views.send_order_shipped_task.delay")
    def test_get_and_repeat_post_do_not_ship_or_notify_twice(self, delay):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(self.url)
            self.client.post(self.url)
        delay.assert_called_once_with(self.order.pk)

    @patch("project.views.send_order_shipped_task.delay")
    def test_other_statuses_are_not_shipped(self, delay):
        for status in ("pending", "cancelled", "shipped"):
            with self.subTest(status=status):
                Order.objects.filter(pk=self.order.pk).update(status=status)
                self.client.post(self.url)
                self.order.refresh_from_db()
                self.assertEqual(self.order.status, status)
        delay.assert_not_called()

    @patch("project.views.send_order_shipped_task.delay")
    def test_rolled_back_shipping_does_not_queue_notification(self, delay):
        with self.captureOnCommitCallbacks(execute=True):
            with self.assertRaisesMessage(ValueError, "rollback"):
                with transaction.atomic():
                    self.client.post(self.url)
                    raise ValueError("rollback")
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")
        delay.assert_not_called()

    @patch(
        "project.views.send_order_shipped_task.delay",
        side_effect=OperationalError("broker unavailable"),
    )
    def test_broker_failure_is_reported_without_claiming_notification(self, delay):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.url)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "shipped")
        messages = [str(message) for message in response.wsgi_request._messages]
        self.assertTrue(any("could not be queued" in message for message in messages))
        delay.assert_called_once_with(self.order.pk)

    def test_missing_order_is_not_found(self):
        self.assertEqual(
            self.client.post(
                reverse("admin-order-confirm-shipped", args=[999999])
            ).status_code,
            404,
        )

    def test_only_shop_managers_can_ship(self):
        self.client.force_login(ProjectUser.objects.create_user(username="other"))
        response = self.client.post(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(ProjectUser.objects.get(username="shipping-manager"))
        self.assertNotEqual(client.post(self.url).status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_management_page_has_post_form_only_for_completed_orders(self):
        other = Order.objects.create(customer=self.customer, status="pending")
        response = self.client.get(self.management_url)
        self.assertContains(response, f'action="{self.url}"')
        self.assertNotContains(
            response, reverse("admin-order-confirm-shipped", args=[other.pk])
        )
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_task_sends_nonempty_text_and_html_shipping_email(self):
        self.order.status = "shipped"
        self.order.save(update_fields=["status"])
        with override("en"):
            self.assertTrue(send_order_shipped_task.run(self.order.pk))
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ["ada@example.com"])
        self.assertIn(str(self.order.pk), email.subject)
        self.assertIn("shipped", email.body.lower())
        self.assertIn("Ada", email.body)
        self.assertIn("Asclepias tuberosa", email.body)
        self.assertIn("Ottawa", email.body)
        self.assertEqual(email.alternatives[0].mimetype, "text/html")
        self.assertIn("Asclepias tuberosa", email.alternatives[0].content)
        self.assertIn("shipped", email.alternatives[0].content.lower())

    def test_shipping_email_logs_each_stage(self):
        with self.assertLogs("project.utils", level="DEBUG") as logs:
            self.assertTrue(send_order_shipped_email(self.order))
        output = "\n".join(logs.output)
        for expected in (
            "Preparing order shipped email",
            "Rendering email templates",
            "Creating email message",
            "Email backend=",
            "Sending order shipped email",
            "Order shipped email sent successfully",
        ):
            self.assertIn(expected, output)
        self.assertIn(f"Order #{self.order.pk}", output)
        self.assertIn("bcc=False", output)

    def test_shipping_email_can_render_in_french(self):
        with override("fr"):
            self.assertTrue(send_order_shipped_task.run(self.order.pk))
        email = mail.outbox[0]
        self.assertIn("expédiée", email.subject)
        self.assertIn("Bonjour Ada,", email.body)
        self.assertIn("expédiée", email.body)
        self.assertIn('lang="fr"', email.alternatives[0].content)
        self.assertIn("expédiée", email.alternatives[0].content)

    @patch("project.views.send_order_shipped_task.delay")
    def test_shipping_view_queues_a_task_that_sends_the_email(self, delay):
        delay.side_effect = lambda order_id: send_order_shipped_task.run(order_id)
        with override("en"), self.captureOnCommitCallbacks(execute=True):
            self.client.post(self.url)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "shipped")
        delay.assert_called_once_with(self.order.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("shipped", mail.outbox[0].subject.lower())

    def test_order_received_email_does_not_claim_order_was_shipped(self):
        with override("en"):
            self.assertTrue(send_order_confirmation_email(self.order))
        self.assertIn("Order received!", mail.outbox[0].alternatives[0].content)
        self.assertNotIn("Order shipped!", mail.outbox[0].alternatives[0].content)

    def test_deleted_order_fails_shipping_task(self):
        order_id = self.order.pk
        self.order.delete()
        with self.assertRaises(Order.DoesNotExist):
            send_order_shipped_task.run(order_id)

    @patch(
        "django.core.mail.EmailMultiAlternatives.send",
        side_effect=RuntimeError("mail failed"),
    )
    def test_shipping_mail_failure_propagates(self, _send):
        with self.assertLogs("project.utils", level="ERROR") as logs:
            with self.assertRaisesRegex(RuntimeError, "mail failed"):
                send_order_shipped_email(self.order)
        self.assertIn(f"Order #{self.order.pk}", logs.output[0])
        self.assertIn("mail failed", logs.output[0])
        _send.assert_called_once()

    @patch("django.core.mail.EmailMultiAlternatives.send", return_value=0)
    def test_shipping_mail_unsent_result_is_a_failure(self, send):
        with self.assertRaisesRegex(RuntimeError, "was not sent"):
            send_order_shipped_task.run(self.order.pk)
        send.assert_called_once()

    def test_shipped_orders_are_in_statistics(self):
        self.order.status = "shipped"
        self.order.save(update_fields=["status"])
        stat = get_order_statistics().get(year=self.order.order_date.year)
        self.assertEqual(stat["shipped_orders"], 1)

    def test_shipped_order_is_already_closed_for_scan_import(self):
        self.order.status = "shipped"
        self.order.save(update_fields=["status"])
        preview = _build_order_scan_import_preview(str(self.order.pk), "scan.txt")
        self.assertEqual(preview["already_closed_order_ids"], [self.order.pk])
        self.assertEqual(preview["closable_order_ids"], [])
