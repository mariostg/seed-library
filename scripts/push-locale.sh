#!/bin/sh

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
SOURCE_LOCALE="$ROOT_DIR/locale/"

if [ ! -f "$ENV_FILE" ]; then
    echo "Missing env file: $ENV_FILE"
    exit 1
fi

. "$ENV_FILE"

if [ -z "$DEVSITE" ] || [ -z "$PRODSITE" ]; then
    echo "DEVSITE and PRODSITE must be set in $ENV_FILE"
    exit 1
fi

usage() {
    echo "Usage: sh scripts/push-locale.sh [dev|prod] [--apply] [--delete] [--confirm-server-write] [--confirm-prod-write]"
    echo ""
    echo "Defaults:"
    echo "  environment: dev"
    echo "  mode: dry-run"
    echo ""
    echo "Examples:"
    echo "  sh scripts/push-locale.sh"
    echo "  sh scripts/push-locale.sh prod"
    echo "  sh scripts/push-locale.sh dev --apply --confirm-server-write"
    echo "  sh scripts/push-locale.sh prod --apply --confirm-server-write --confirm-prod-write"
    echo "  sh scripts/push-locale.sh prod --apply --delete --confirm-server-write --confirm-prod-write"
}

ENV_NAME="dev"
DRY_RUN=1
DELETE_REMOTE_MISSING=0
CONFIRM_SERVER_WRITE=0
CONFIRM_PROD_WRITE=0

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
        --confirm-server-write)
            CONFIRM_SERVER_WRITE=1
            ;;
        --confirm-prod-write)
            CONFIRM_PROD_WRITE=1
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

if [ "$DRY_RUN" -eq 0 ] && [ "$CONFIRM_SERVER_WRITE" -ne 1 ]; then
    echo "WARNING: --apply writes local locale files to the server."
    echo "Refusing to continue without explicit confirmation flag: --confirm-server-write"
    exit 1
fi

if [ "$DRY_RUN" -eq 0 ] && [ "$ENV_NAME" = "prod" ] && [ "$CONFIRM_PROD_WRITE" -ne 1 ]; then
    echo "WARNING: production locale files may be overwritten."
    echo "Refusing to continue without explicit confirmation flag: --confirm-prod-write"
    exit 1
fi

if [ "$ENV_NAME" = "prod" ]; then
    REMOTE_SITE="$PRODSITE"
else
    REMOTE_SITE="$DEVSITE"
fi

TARGET_LOCALE="$REMOTE_SITE/locale/"
DRY_RUN_FLAG=""
DELETE_FLAG=""

if [ "$DRY_RUN" -eq 1 ]; then
    DRY_RUN_FLAG="--dry-run"
fi

if [ "$DELETE_REMOTE_MISSING" -eq 1 ]; then
    DELETE_FLAG="--delete"
fi

echo "Sync source: $SOURCE_LOCALE"
echo "Sync target: $TARGET_LOCALE"

if [ "$DRY_RUN" -eq 1 ]; then
    echo "Mode: dry-run (no server files will be changed)."
else
    echo "WARNING: this operation updates server locale files."
    echo "Mode: apply (server locale files will be updated)."
fi

if [ "$DELETE_REMOTE_MISSING" -eq 1 ]; then
    echo "Delete mode: enabled (server files missing locally will be removed)."
fi

rsync -avz $DRY_RUN_FLAG $DELETE_FLAG "$SOURCE_LOCALE" "$TARGET_LOCALE"

echo "--------------------"
if [ "$DRY_RUN" -eq 1 ]; then
    echo "Dry-run completed."
    echo "Run with --apply to update server locale files."
else
    echo "Locale push completed."
    echo "If needed on server, run: python manage.py compilemessages"
fi
echo "--------------------"
