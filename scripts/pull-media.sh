#!/bin/sh
# This script pulls plant images located at media/project/images/plants from the remote server to the local machine.

usage() {
	echo "Usage: sh scripts/pull-media.sh [--dry-run|-n] [--delete]"
	echo
	echo "Options:"
	echo "  --dry-run, -n   Show what would be transferred without changing local files"
	echo "  --delete        Delete local files not present on the remote source"
	echo "  --help, -h      Show this help message"
}

DRY_RUN=0
DELETE=0

while [ "$#" -gt 0 ]; do
	case "$1" in
		--dry-run|-n)
			DRY_RUN=1
			;;
		--delete)
			DELETE=1
			;;
		--help|-h)
			usage
			exit 0
			;;
		*)
			echo "Unknown option: $1"
			echo
			usage
			exit 1
			;;
	esac
	shift
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ENV_FILE="$SCRIPT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
	# shellcheck disable=SC1090
	. "$ENV_FILE"
fi

: "${REMOTE_USER:?REMOTE_USER is not set. Define it in scripts/.env}"
: "${REMOTE_HOST:?REMOTE_HOST is not set. Define it in scripts/.env}"
: "${REMOTE_PATH:?REMOTE_PATH is not set. Define it in scripts/.env}"
: "${LOCAL_PATH:=media/project/images/plants}"

RSYNC_ARGS="-avz --progress"
if [ "$DRY_RUN" -eq 1 ]; then
	RSYNC_ARGS="$RSYNC_ARGS --dry-run"
	echo "Running in dry-run mode (no files will be modified)."
fi
if [ "$DELETE" -eq 1 ]; then
	RSYNC_ARGS="$RSYNC_ARGS --delete"
	echo "Delete mode enabled (local files missing on remote will be removed)."
fi

echo "Source: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"
echo "Target: ${LOCAL_PATH}/"

rsync $RSYNC_ARGS "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/" "${LOCAL_PATH}/"
