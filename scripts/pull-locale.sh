#!/bin/sh

DEVSITE='mariost-gelais@mariostg.com:~/owsl.mariostg.com'
PRODSITE='mariost-gelais@mariostg.com:~/catalogue.wildflowerseedlibrary.ca'

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
TARGET_LOCALE="$ROOT_DIR/locale/"

usage() {
    echo "Usage: sh scripts/pull-locale.sh [dev|prod] [--apply] [--delete]"
    echo ""
    echo "Defaults:"
    echo "  environment: dev"
    echo "  mode: dry-run"
    echo ""
    echo "Examples:"
    echo "  sh scripts/pull-locale.sh"
    echo "  sh scripts/pull-locale.sh prod"
    echo "  sh scripts/pull-locale.sh prod --apply"
    echo "  sh scripts/pull-locale.sh prod --apply --delete"
}

ENV_NAME="dev"
DRY_RUN=1
DELETE_REMOTE_MISSING=0

for arg in "$@"; do
    case "$arg" in
        dev|prod)
            ENV_NAME="$arg"
            ;;
        --apply)
            DRY_RUN=0
            ;;
        --delete)
            DELETE_REMOTE_MISSING=1
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Invalid argument: $arg"
            usage
            exit 1
            ;;
    esac
done

if [ "$ENV_NAME" = "prod" ]; then
    REMOTE_SITE="$PRODSITE"
else
    REMOTE_SITE="$DEVSITE"
fi

REMOTE_LOCALE="$REMOTE_SITE/locale/"
DRY_RUN_FLAG=""
DELETE_FLAG=""

if [ "$DRY_RUN" -eq 1 ]; then
    DRY_RUN_FLAG="--dry-run"
fi

if [ "$DELETE_REMOTE_MISSING" -eq 1 ]; then
    DELETE_FLAG="--delete"
fi

echo "Sync source: $REMOTE_LOCALE"
echo "Sync target: $TARGET_LOCALE"

if [ "$DRY_RUN" -eq 1 ]; then
    echo "Mode: dry-run (no local files will be changed)."
else
    echo "Mode: apply (local locale files will be updated)."
fi

if [ "$DELETE_REMOTE_MISSING" -eq 1 ]; then
    echo "Delete mode: enabled (local files missing from server will be removed)."
fi

rsync -avz $DRY_RUN_FLAG $DELETE_FLAG "$REMOTE_LOCALE" "$TARGET_LOCALE"

echo "--------------------"
if [ "$DRY_RUN" -eq 1 ]; then
    echo "Dry-run completed."
    echo "Run with --apply to update local locale files."
else
    echo "Locale pull completed."
    echo "Review changes then commit locale/*.po and locale/*.mo to GitHub."
fi
echo "--------------------"
