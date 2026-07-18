from unittest.mock import patch

from django.test import TransactionTestCase

from project import utils
from project.models import Customer, PlantProfile, ShoppingCart


class OrderCeleryEnqueueTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            address="1 Test St",
            city="City",
            province="State",
            postal_code="00000",
        )

        self.plant = PlantProfile.objects.create(latin_name="Testus plantus")

        ShoppingCart.objects.create(
            customer=self.customer, plant_profile=self.plant, quantity=2
        )

    def _make_request(self):
        # create a lightweight request-like object with a session dict
        class R:
            pass

        r = R()
        r.session = {"customer_id": self.customer.id}
        return r

    @patch("project.tasks.send_order_confirmation_task.delay")
    @patch("project.tasks.send_donation_thank_you_task.delay")
    def test_order_enqueue_tasks_without_donation(
        self, mock_donation_delay, mock_confirm_delay
    ):
        request = self._make_request()

        order = utils.create_order_from_cart(request, donation_amount=0)

        # ensure an order was created
        self.assertIsNotNone(order)

        # send_order_confirmation_task.delay should be enqueued once with order.id
        mock_confirm_delay.assert_called_once_with(order.id)
        # donation should not be enqueued
        mock_donation_delay.assert_not_called()

    @patch("project.tasks.send_order_confirmation_task.delay")
    @patch("project.tasks.send_donation_thank_you_task.delay")
    def test_order_enqueue_tasks_with_donation(
        self, mock_donation_delay, mock_confirm_delay
    ):
        request = self._make_request()

        order = utils.create_order_from_cart(request, donation_amount=5.0)

        self.assertIsNotNone(order)

        mock_confirm_delay.assert_called_once_with(order.id)
        mock_donation_delay.assert_called_once_with(order.id)
