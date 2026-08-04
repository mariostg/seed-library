from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError

from project.email_security import decrypt_email
from project.models import Customer, ProjectUser

try:
    from cryptography.fernet import InvalidToken
except Exception:  # pragma: no cover
    InvalidToken = ValueError


class Command(BaseCommand):
    help = "Validate encrypted email tokens for customers and users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--scope",
            choices=["customers", "users", "all"],
            default="customers",
            help="Choose which encrypted email fields to validate.",
        )
        parser.add_argument(
            "--fail-on-invalid",
            action="store_true",
            help="Raise an error when one or more invalid tokens are found.",
        )

    def handle(self, *args, **options):
        scope = options["scope"]
        fail_on_invalid = options["fail_on_invalid"]

        total_checked = 0
        total_invalid = 0

        if scope in {"customers", "all"}:
            checked, invalid = self._scan_queryset(
                label="Customer",
                queryset=Customer.objects.exclude(email_encrypted="").values_list(
                    "id", "email_encrypted"
                ),
            )
            total_checked += checked
            total_invalid += len(invalid)
            self._write_scope_report("customers", checked, invalid)

        if scope in {"users", "all"}:
            checked, invalid = self._scan_queryset(
                label="ProjectUser",
                queryset=ProjectUser.objects.exclude(email_encrypted="").values_list(
                    "id", "email_encrypted"
                ),
            )
            total_checked += checked
            total_invalid += len(invalid)
            self._write_scope_report("users", checked, invalid)

        summary = (
            f"Validation complete. Checked {total_checked} encrypted email token(s); "
            f"found {total_invalid} invalid token(s)."
        )

        if total_invalid and fail_on_invalid:
            raise CommandError(
                f"Invalid encrypted email token(s) found: {total_invalid}"
            )

        self.stdout.write(summary)

    def _scan_queryset(self, label, queryset):
        checked = 0
        invalid = []

        try:
            for object_id, token in queryset.iterator(chunk_size=500):
                checked += 1
                try:
                    decrypt_email(token)
                except InvalidToken:
                    invalid.append(f"{label} id={object_id}")
        except ImproperlyConfigured as exc:
            raise CommandError(str(exc)) from exc

        return checked, invalid

    def _write_scope_report(self, scope_name, checked, invalid):
        self.stdout.write(
            f"[{scope_name}] checked {checked} encrypted email token(s); "
            f"invalid token(s): {len(invalid)}"
        )
        for entry in invalid:
            self.stdout.write(self.style.WARNING(f"  - {entry} has an invalid token"))
