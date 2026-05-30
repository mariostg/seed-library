#!/bin/sh

# One-way sync of Rosetta-managed translation files from server to local repo.
# Server is source of truth. This script never pushes locale files to server.

DEVSITE='mariost-gelais@mariostg.com:~/owsl.mariostg.com'
PRODSITE='mariost-gelais@mariostg.com:~/catalogue.wildflowerseedlibrary.ca'

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
TARGET_LOCALE="$ROOT_DIR/locale/"

usage() {
    echo "Usage: sh scripts/sync-rosetta-po.sh [dev|prod] [--apply] [--delete] [--include-mo]"
    echo ""
    echo "Purpose:"
    echo "  Pull Rosetta-managed translation files from server to local locale/."
    echo "  This script is one-way only (server -> local)."
    echo ""
    echo "Defaults:"
    echo "  environment: dev"
    echo "  mode: dry-run"
    echo "  files: .po only"
    echo ""
    echo "Examples:"
    echo "  sh scripts/sync-rosetta-po.sh"
    echo "  sh scripts/sync-rosetta-po.sh prod"
    echo "  sh scripts/sync-rosetta-po.sh prod --apply"
    echo "  sh scripts/sync-rosetta-po.sh prod --apply --delete"
    echo "  sh scripts/sync-rosetta-po.sh prod --apply --include-mo"
}

ENV_NAME="dev"
DRY_RUN=1
DELETE_REMOTE_MISSING=0
INCLUDE_MO=0

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
        --include-mo)
            INCLUDE_MO=1
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

echo "Rosetta locale sync (server -> local)"
echo "Source: $REMOTE_LOCALE"
echo "Target: $TARGET_LOCALE"

if [ "$DRY_RUN" -eq 1 ]; then
    echo "Mode: dry-run (no local files will be changed)."
else
    echo "Mode: apply (local files will be updated)."
fi

if [ "$DELETE_REMOTE_MISSING" -eq 1 ]; then
    echo "Delete mode: enabled (local files missing from server will be removed)."
fi

if [ "$INCLUDE_MO" -eq 1 ]; then
    echo "File mode: syncing .po and .mo files."
else
    echo "File mode: syncing .po files only."
fi

# Restrict transfer to translation files and directory structure.
if [ "$INCLUDE_MO" -eq 1 ]; then
    rsync -avz $DRY_RUN_FLAG $DELETE_FLAG \
        --include='*/' \
        --include='*.po' \
        --include='*.mo' \
        --exclude='*' \
        "$REMOTE_LOCALE" "$TARGET_LOCALE"
else
    rsync -avz $DRY_RUN_FLAG $DELETE_FLAG \
        --include='*/' \
        --include='*.po' \
        --exclude='*' \
        "$REMOTE_LOCALE" "$TARGET_LOCALE"
fi

echo "--------------------"
if [ "$DRY_RUN" -eq 1 ]; then
    echo "Dry-run completed."
    echo "Run with --apply to update local translation files."
else
    echo "Sync completed."
    echo "Next steps:"
    echo "  1) git status"
    echo "  2) git add locale/**/*.po"
    if [ "$INCLUDE_MO" -eq 1 ]; then
        echo "  3) git add locale/**/*.mo"
    fi
    echo "  4) git commit -m 'Sync Rosetta locale from server'"
    echo "  5) git push"
fi
echo "--------------------"
