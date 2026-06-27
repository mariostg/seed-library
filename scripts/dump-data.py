#!/usr/bin/env python3
"""Dump selected Django models into JSON fixtures for deployment/migration workflows.

Usage examples:
  scripts/dump-data.py
  scripts/dump-data.py --database default --output-dir scripts/data --clean
  scripts/dump-data.py --continue-on-error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = BASE_DIR / "scripts" / "data"

# Export order is intentional: reference/lookup models first, then core models.
MODEL_LABELS = [
    "auth.group",
    "auth.permission",
    "project.beespecies",
    "project.bloomcolour",
    "project.butterflyspecies",
    "project.conservationstatus",
    "project.ecozone",
    "project.growthhabit",
    "project.harvestingindicator",
    "project.harvestingmean",
    "project.lighting",
    "project.narrativetype",
    "project.nonnativespecies",
    "project.obsoletenames",
    "project.onecultivar",
    "project.packagingmeasure",
    "project.plantlifespan",
    "project.plantmorphology",
    "project.seedeventtable",
    "project.seedhead",
    "project.seedpreparation",
    "project.seedstorage",
    "project.seedstoragelabelinfo",
    "project.seedviabilitytest",
    "project.sowingdepth",
    "project.stratificationduration",
    "project.toxicityindicator",
    "project.plantcollection",
    "project.plantcomplementary",
    "project.plantprofile",
    "project.plantnarrative",
    "project.plantimage",
    "project.projectuser",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dump selected models to JSON fixtures for deployment."
    )
    parser.add_argument(
        "--database",
        default="default",
        help="Django database alias (default: default)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing JSON files in output dir before dump.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue dumping other models if one model fails.",
    )
    return parser.parse_args()


def setup_django() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    sys.path.insert(0, str(BASE_DIR))
    import django

    django.setup()


def model_label_to_filename(model_label: str) -> str:
    return model_label.replace(".", "_") + ".json"


def validate_models(model_labels: list[str]) -> None:
    from django.apps import apps

    missing = []
    for label in model_labels:
        if apps.get_model(label) is None:
            missing.append(label)
    if missing:
        raise SystemExit(
            "Invalid model labels in dump configuration: " + ", ".join(missing)
        )


def clean_output_dir(output_dir: Path) -> None:
    for file_path in output_dir.glob("*.json"):
        file_path.unlink()


def dump_model(
    *, model_label: str, output_file: Path, database: str, indent: int
) -> int:
    from django.core.management import call_command

    with output_file.open("w", encoding="utf-8") as handle:
        call_command(
            "dumpdata",
            model_label,
            database=database,
            indent=indent,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
            stdout=handle,
        )

    with output_file.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return len(payload)


def main() -> int:
    args = parse_args()
    setup_django()

    from django.core.management.base import CommandError

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.clean:
        clean_output_dir(output_dir)

    validate_models(MODEL_LABELS)

    failures: list[tuple[str, str]] = []
    total_objects = 0

    print(f"Dumping data to: {output_dir}")
    print(f"Using database alias: {args.database}")

    for model_label in MODEL_LABELS:
        output_file = output_dir / model_label_to_filename(model_label)
        try:
            count = dump_model(
                model_label=model_label,
                output_file=output_file,
                database=args.database,
                indent=args.indent,
            )
            total_objects += count
            print(f"OK  {model_label:<40} -> {output_file.name} ({count} rows)")
        except (CommandError, OSError, json.JSONDecodeError) as exc:
            failures.append((model_label, str(exc)))
            print(f"ERR {model_label:<40} -> {exc}")
            if not args.continue_on_error:
                break
        except KeyboardInterrupt:
            print("Interrupted by user.")
            return 130

    print("\nSummary")
    print(f"  Models attempted: {len(MODEL_LABELS)}")
    print(f"  Total rows dumped: {total_objects}")
    print(f"  Failures: {len(failures)}")

    if failures:
        for model_label, error in failures:
            print(f"  - {model_label}: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
