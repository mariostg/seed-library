# Media Archive Backup (Snapshot + Retention)

This project includes `scripts/backup-media-archive.sh` to back up `media/` as timestamped `.tar.gz` snapshots to a remote server.

## Why this mode

- Keeps historical backups (point-in-time snapshots)
- Protects against accidental source deletions
- Keeps a short local archive history for quick recovery
- Supports retention cleanup on destination (`RETENTION_DAYS`, `RETENTION_COUNT`)
- Skips archive creation/upload when source content has not changed

## One-time setup

```bash
chmod +x scripts/backup-media-archive.sh
```

## Required variable

- `ARCHIVE_DEST` in format `user@host:/remote/path`

Example:

```bash
ARCHIVE_DEST='backup@203.0.113.10:/home/django/backups/owsl/media-archives' \
./scripts/backup-media-archive.sh --verbose
```

## Optional variables

- `MEDIA_DIR` (default: `./media`)
- `STATE_DIR` (default: `./.backup-state`)
- `TMP_DIR` (default: `./.backup-state/tmp`)
- `LOCAL_RETENTION_DAYS` (default: `5`)
- `SSH_PORT` (optional)
- `RETENTION_DAYS` (default: `30`)
- `RETENTION_COUNT` (default: `30`)

## Options

- `--force`: create/upload snapshot even with no detected changes
- `--dry-run`: show actions without changing anything
- `--verbose`: print detailed progress

## Cron example

Daily at 03:00:

```cron
IP='203.0.113.10'
BASE_DIR='/path/to/djbp'
BACKUP_FOLDER='/srv/backups/owsl/media-archives'
LOG_FILE="$BASE_DIR/logs/media-archive-backup.log"

0 3 * * * cd "$BASE_DIR" && ARCHIVE_DEST="backup@${IP}:${BACKUP_FOLDER}" RETENTION_DAYS=30 RETENTION_COUNT=60 ./scripts/backup-media-archive.sh >> "$LOG_FILE" 2>&1
```

## Notes

- Configure SSH key auth for unattended cron runs.
- The script stores a local fingerprint in `./.backup-state/media-archive.fingerprint`.
- The uploaded archive filename format is `media-YYYYMMDD-HHMMSS.tar.gz`.
- Local archives are kept under `TMP_DIR` and pruned when older than `LOCAL_RETENTION_DAYS`.
