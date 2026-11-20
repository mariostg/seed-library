from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils import timezone
from django.utils.translation import override

from project import tasks, views


class GeneratedOrdersPdfCleanupTests(SimpleTestCase):
    @patch("project.tasks.default_storage")
    def test_cleanup_deletes_only_files_older_than_retention(self, mock_storage):
        now = timezone.now()
        old_time = now - timedelta(days=3)
        recent_time = now - timedelta(hours=12)

        def listdir_side_effect(path):
            if path == settings.GENERATED_ORDERS_PDF_DIR:
                return (["nested"], ["old.pdf", "recent.pdf"])
            if path == f"{settings.GENERATED_ORDERS_PDF_DIR}/nested":
                return ([], ["old_nested.pdf"])
            return ([], [])

        def modified_side_effect(path):
            if path.endswith("recent.pdf"):
                return recent_time
            return old_time

        mock_storage.listdir.side_effect = listdir_side_effect
        mock_storage.get_modified_time.side_effect = modified_side_effect

        deleted_count = tasks.cleanup_generated_orders_pdfs(retention_days=1)

        self.assertEqual(deleted_count, 2)
        mock_storage.delete.assert_any_call(
            f"{settings.GENERATED_ORDERS_PDF_DIR}/old.pdf"
        )
        mock_storage.delete.assert_any_call(
            f"{settings.GENERATED_ORDERS_PDF_DIR}/nested/old_nested.pdf"
        )
        self.assertEqual(mock_storage.delete.call_count, 2)

    @patch("project.tasks.cleanup_generated_orders_pdfs")
    def test_cleanup_task_wrapper_passes_retention_days(self, mock_cleanup):
        mock_cleanup.return_value = 4

        result = tasks.cleanup_generated_orders_pdfs_task(retention_days=5)

        self.assertEqual(result, 4)
        mock_cleanup.assert_called_once_with(retention_days=5)

    @override_settings(ORDERS_PDF_RETENTION_DAYS=3)
    def test_notice_uses_configured_retention(self):
        request = RequestFactory().get("/")
        with override("en"), patch(
            "project.views.utils.get_generated_filtered_orders_pdfs", return_value=[]
        ):
            response = views.admin_order_list_generated_pdfs.__wrapped__(request)
        self.assertContains(response, "Generated PDFs older than 3 days")
        self.assertContains(response, "Download a copy to your computer")

    @override_settings(ORDERS_PDF_RETENTION_DAYS=1)
    def test_notice_uses_singular_for_one_day(self):
        request = RequestFactory().get("/")
        with override("en"), patch(
            "project.views.utils.get_generated_filtered_orders_pdfs", return_value=[]
        ):
            response = views.admin_order_list_generated_pdfs.__wrapped__(request)
        self.assertContains(response, "Generated PDFs older than 1 day are deleted")

    @override_settings(PENDING_ORDERS_PDF_RETENTION_DAYS=5)
    def test_retention_uses_legacy_setting(self):
        self.assertEqual(tasks.get_orders_pdf_retention_days(), 5)
