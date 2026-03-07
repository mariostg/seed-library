#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MEDIA_DIR="${MEDIA_DIR:-$BASE_DIR/media}"
STATE_DIR="${STATE_DIR:-$BASE_DIR/.backup-state}"
STATE_FILE="$STATE_DIR/media-archive.fingerprint"
TMP_DIR="${TMP_DIR:-$STATE_DIR/tmp}"

FORCE=0
DRY_RUN=0
VERBOSE=0

usage() {
  cat <<'EOF'
Usage: scripts/backup-media-archive.sh [--force] [--dry-run] [--verbose]

Creates a timestamped media archive (tar.gz), uploads it to a remote server,
and prunes older archives on destination by retention policy.

Environment variables:
  ARCHIVE_DEST      Required. Destination in form user@host:/remote/path
  MEDIA_DIR         Optional. Defaults to ./media
  STATE_DIR         Optional. Defaults to ./.backup-state
  TMP_DIR           Optional. Defaults to ./.backup-state/tmp
  LOCAL_RETENTION_DAYS Optional. Delete local archives older than N days (default: 5)
  SSH_PORT          Optional. SSH port for upload and cleanup
  RETENTION_DAYS    Optional. Delete archives older than N days (default: 30)
  RETENTION_COUNT   Optional. Keep only N most recent archives (default: 30)

Options:
  --force           Create/upload archive even when no source change detected
  --dry-run         Show what would run, do not create/upload/delete
  --verbose         More output
  -h, --help        Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
    --verbose)
      VERBOSE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

if [[ ! -d "$MEDIA_DIR" ]]; then
  echo "Media directory not found: $MEDIA_DIR" >&2
  exit 1
fi

MEDIA_DIR_ABS="$(cd "$MEDIA_DIR" && pwd)"

if [[ -z "${ARCHIVE_DEST:-}" ]]; then
  echo "ARCHIVE_DEST is required (example: user@203.0.113.10:/srv/backups/owsl/media-archives)" >&2
  exit 1
fi

if [[ "$ARCHIVE_DEST" != *:* ]]; then
  echo "ARCHIVE_DEST must be in the format user@host:/remote/path" >&2
  exit 1
fi

RETENTION_DAYS="${RETENTION_DAYS:-30}"
RETENTION_COUNT="${RETENTION_COUNT:-30}"
LOCAL_RETENTION_DAYS="${LOCAL_RETENTION_DAYS:-5}"

mkdir -p "$STATE_DIR" "$TMP_DIR"

fingerprint="$({
  printf 'MEDIA_DIR=%s\n' "$MEDIA_DIR"
  find "$MEDIA_DIR" -type f -print0 | sort -z | \
    xargs -0 shasum -a 256 2>/dev/null || true
} | shasum -a 256 | awk '{print $1}')"

previous_fingerprint=""
if [[ -f "$STATE_FILE" ]]; then
  previous_fingerprint="$(cat "$STATE_FILE")"
fi

if [[ $FORCE -eq 0 && "$fingerprint" == "$previous_fingerprint" ]]; then
  echo "No changes detected in $MEDIA_DIR. Skipping archive backup."
  exit 0
fi

timestamp="$(date +%Y%m%d-%H%M%S)"
archive_name="media-${timestamp}.tar.gz"
archive_path="$TMP_DIR/$archive_name"

remote_host="${ARCHIVE_DEST%%:*}"
remote_path="${ARCHIVE_DEST#*:}"

ssh_cmd=(ssh)
if [[ -n "${SSH_PORT:-}" ]]; then
  ssh_cmd+=( -p "$SSH_PORT" )
fi

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[dry-run] Would create archive: $archive_path"
  echo "[dry-run] Would upload to: $ARCHIVE_DEST/$archive_name"
  echo "[dry-run] Would prune local archives in $TMP_DIR older than $LOCAL_RETENTION_DAYS days"
  echo "[dry-run] Would prune by days > $RETENTION_DAYS and keep latest $RETENTION_COUNT archives"
  exit 0
fi

if [[ $VERBOSE -eq 1 ]]; then
  echo "Creating archive $archive_path from $MEDIA_DIR"
fi
tar -czf "$archive_path" -C "$(dirname "$MEDIA_DIR_ABS")" "$(basename "$MEDIA_DIR_ABS")"

rsync_flags=(-az)
[[ $VERBOSE -eq 1 ]] && rsync_flags+=(-v)

if [[ $VERBOSE -eq 1 ]]; then
  echo "Uploading archive to $ARCHIVE_DEST"
fi
rsync "${rsync_flags[@]}" --rsh "${ssh_cmd[*]}" "$archive_path" "$ARCHIVE_DEST/"

remote_file="$remote_path/$archive_name"

cleanup_script=$(cat <<'EOS'
set -euo pipefail
remote_path="$1"
retention_days="$2"
retention_count="$3"

mkdir -p "$remote_path"
find "$remote_path" -maxdepth 1 -type f -name 'media-*.tar.gz' -mtime "+$retention_days" -delete

if [[ "$retention_count" -gt 0 ]]; then
  old_files="$(ls -1t "$remote_path"/media-*.tar.gz 2>/dev/null | tail -n +$((retention_count + 1)) || true)"
  if [[ -n "$old_files" ]]; then
    while IFS= read -r file; do
      [[ -n "$file" ]] && rm -f -- "$file"
    done <<< "$old_files"
  fi
fi
EOS
)

if [[ $VERBOSE -eq 1 ]]; then
  echo "Applying retention on remote path $remote_path"
fi
"${ssh_cmd[@]}" "$remote_host" bash -s -- "$remote_path" "$RETENTION_DAYS" "$RETENTION_COUNT" <<< "$cleanup_script"

printf '%s' "$fingerprint" > "$STATE_FILE"

# Keep local archives for a short period for quick recovery and prune old files.
find "$TMP_DIR" -maxdepth 1 -type f -name 'media-*.tar.gz' -mtime "+$LOCAL_RETENTION_DAYS" -delete

echo "Archive backup complete: $remote_file"
echo "State updated: $STATE_FILE"
