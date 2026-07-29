from datetime import timedelta
from unittest.mock import patch

from django.test import SimpleTestCase
from django.utils import timezone

from project import tasks


class GeneratedOrdersPdfCleanupTests(SimpleTestCase):
    @patch("project.tasks.default_storage")
    def test_cleanup_deletes_only_files_older_than_retention(self, mock_storage):
        now = timezone.now()
        old_time = now - timedelta(days=3)
        recent_time = now - timedelta(hours=12)

        def listdir_side_effect(path):
            if path == tasks.GENERATED_ORDERS_PDF_DIR:
                return (["nested"], ["old.pdf", "recent.pdf"])
            if path == f"{tasks.GENERATED_ORDERS_PDF_DIR}/nested":
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
        mock_storage.delete.assert_any_call(f"{tasks.GENERATED_ORDERS_PDF_DIR}/old.pdf")
        mock_storage.delete.assert_any_call(
            f"{tasks.GENERATED_ORDERS_PDF_DIR}/nested/old_nested.pdf"
        )
        self.assertEqual(mock_storage.delete.call_count, 2)

    @patch("project.tasks.cleanup_generated_orders_pdfs")
    def test_cleanup_task_wrapper_passes_retention_days(self, mock_cleanup):
        mock_cleanup.return_value = 4

        result = tasks.cleanup_generated_orders_pdfs_task(retention_days=5)

        self.assertEqual(result, 4)
        mock_cleanup.assert_called_once_with(retention_days=5)
