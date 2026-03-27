#!/usr/bin/env bash

# This script is intended to be run as a cron job on the server hosting the media archive.
# It performs a backup of the media archive to a remote server, ensuring that only one instance runs at a time using a lock file.
# The backup script is expected to handle the actual backup process, including retention policies for old backups.
# The script logs its activity to a specified log file, including timestamps for the start and end of the backup process.
# Usage:
#   1. Ensure that the backup script (backup-media-archive.sh) is executable and properly configured to perform the backup.
#   2. Set up a cron job to run this script at the desired frequency (e.g., daily at 2 AM):
# SHELL=/bin/bash
# PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# 0 2 * * * /path/to/run-media-archive-backup.sh


set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="${MEDIA_ARCHIVE_ENV_FILE:-$SCRIPT_DIR/.env.media-archive}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE" >&2
  echo "Create it from scripts/.env.media-archive.example" >&2
  exit 1
fi

# Load deployment-specific values without exposing them in source control.
set -a
source "$ENV_FILE"
set +a

: "${IP:?IP is required in $ENV_FILE}"
: "${BACKUP_FOLDER:?BACKUP_FOLDER is required in $ENV_FILE}"

SSH_USER="${SSH_USER:-django}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
RETENTION_COUNT="${RETENTION_COUNT:-60}"
LOG_FILE="${LOG_FILE:-$BASE_DIR/logs/media-archive-backup.log}"
LOCK_FILE="${LOCK_FILE:-/tmp/owsl-media-archive-backup.lock}"

mkdir -p "$BASE_DIR/logs"

{
  echo "[$(date -Is)] START media archive backup"

  cd "$BASE_DIR"
  ARCHIVE_DEST="${SSH_USER}@${IP}:${BACKUP_FOLDER}" \
  RETENTION_DAYS="$RETENTION_DAYS" \
  RETENTION_COUNT="$RETENTION_COUNT" \
  flock -n "$LOCK_FILE" "$BASE_DIR/scripts/backup-media-archive.sh"
  rc=$?

  echo "[$(date -Is)] END media archive backup (exit=$rc)"
  exit "$rc"
} >> "$LOG_FILE" 2>&1
