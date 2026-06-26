import argparse
from dataclasses import dataclass
from textwrap import indent

from django.core.management.base import BaseCommand, CommandError

from project import models


@dataclass(frozen=True)
class PlantProfileCheck:
    name: str
    description: str


class Command(BaseCommand):
    help = "Analyze plant profiles and report data consistency issues."
    missing_args_message = ""

    def create_parser(self, prog_name, subcommand, **kwargs):
        kwargs.setdefault("formatter_class", argparse.RawTextHelpFormatter)
        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser):
        checks = self.get_checks()
        parser.epilog = self.format_available_checks(checks)
        parser.add_argument(
            "--check",
            action="append",
            dest="checks",
            help=(
                "Run only the named check. Can be provided multiple times.\n"
                "Available checks:\n" + indent("\n".join(sorted(checks.keys())), "  ")
            ),
        )
        parser.add_argument(
            "--fail-on-issues",
            action="store_true",
            help="Raise an error when one or more issues are found.",
        )

    def handle(self, *args, **options):
        checks = self.get_checks()
        selected_checks = options["checks"] or []

        if selected_checks:
            unknown_checks = sorted(set(selected_checks) - checks.keys())
            if unknown_checks:
                valid_checks = ", ".join(sorted(checks.keys()))
                raise CommandError(
                    f"Unknown check(s): {', '.join(unknown_checks)}. Valid checks: {valid_checks}"
                )
            checks = {name: checks[name] for name in selected_checks}

        self.stdout.write("Analyzing plant profiles...")

        total_issues = 0
        for name, check in checks.items():
            self.stdout.write(f"[{name}] {check.description}")
            issues = self.run_check(name)
            if issues:
                total_issues += len(issues)
                for issue in issues:
                    self.stdout.write(self.style.WARNING(f"  - {issue}"))
            else:
                self.stdout.write(self.style.SUCCESS("  No issues found."))

        summary = f"Plant profile analysis completed. {total_issues} issue(s) found."
        if total_issues and options["fail_on_issues"]:
            raise CommandError(summary)

        self.stdout.write(summary)

    def get_checks(self):
        return {
            "double_dormancy_requires_stratification": PlantProfileCheck(
                name="double_dormancy_requires_stratification",
                description=(
                    "Plants with double dormancy must have a stratification duration."
                ),
            ),
            "missing_taxon": PlantProfileCheck(
                name="missing_taxon",
                description="Plants must have a taxon identifier for VASCAN.",
            ),
            "missing_inaturalist_taxon": PlantProfileCheck(
                name="missing_inaturalist_taxon",
                description="Plants must have an iNaturalist taxon identifier.",
            ),
        }

    def format_available_checks(self, checks):
        lines = ["Available checks:"]
        for name, check in checks.items():
            lines.append(f"  {name}: {check.description}")
        return "\n".join(lines)

    def run_check(self, name):
        method_name = f"check_{name}"
        return getattr(self, method_name)()

    def check_double_dormancy_requires_stratification(self):
        plants = models.PlantProfile.all_objects.filter(
            double_dormancy=True,
            stratification_duration__isnull=True,
        ).order_by("latin_name")

        return [
            f"Plant '{plant.latin_name}' (ID: {plant.pk}) has double dormancy but no stratification duration."
            for plant in plants
        ]

    def check_missing_taxon(self):
        plants = models.PlantProfile.all_objects.filter(
            taxon="",
        ).order_by("latin_name")

        return [
            f"Plant '{plant.latin_name}' (ID: {plant.pk}) is missing a taxon."
            for plant in plants
        ]

    def check_missing_inaturalist_taxon(self):
        plants = models.PlantProfile.all_objects.filter(
            inaturalist_taxon="",
        ).order_by("latin_name")

        return [
            f"Plant '{plant.latin_name}' (ID: {plant.pk}) is missing an iNaturalist taxon."
            for plant in plants
        ]
