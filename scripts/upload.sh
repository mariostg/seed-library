#!/bin/sh
# Load deployment targets from scripts/.env, regardless of current working directory.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Missing env file: $ENV_FILE"
    exit 1
fi

. "$ENV_FILE"

if [ -z "$DEVSITE" ] || [ -z "$PRODSITE" ]; then
    echo "DEVSITE and PRODSITE must be set in $ENV_FILE"
    exit 1
fi

SOURCE="."
LOCALROOT=$(pwd)

diff_remote_file() {
    target_spec="$1"
    relpath="$2"

    if [ -z "$relpath" ]; then
        echo "Usage: ./upload.sh diff-dev <relative/path/to/file>"
        echo "   or: ./upload.sh diff-prod <relative/path/to/file>"
        exit 1
    fi

    local_file="$LOCALROOT/$relpath"
    if [ ! -f "$local_file" ]; then
        echo "Local file not found: $local_file"
        exit 1
    fi

    remote_host="${target_spec%%:*}"
    remote_base="${target_spec#*:}"
    if [ -z "$remote_host" ] || [ -z "$remote_base" ] || [ "$remote_host" = "$target_spec" ]; then
        echo "Invalid remote target: $target_spec"
        exit 1
    fi

    echo "Comparing local and remote file: $relpath"
    tmp_remote_file=$(mktemp)
    if [ $? -ne 0 ]; then
        echo "Failed to create temp file"
        exit 1
    fi

    ssh "$remote_host" "cat $remote_base/$relpath" > "$tmp_remote_file"
    if [ $? -ne 0 ]; then
        echo "Failed to read remote file: $remote_base/$relpath"
        rm -f "$tmp_remote_file"
        exit 1
    fi

    diff -u "$local_file" "$tmp_remote_file"
    diff_exit_code=$?
    rm -f "$tmp_remote_file"

    if [ $diff_exit_code -eq 0 ]; then
        echo "No differences found."
    elif [ $diff_exit_code -eq 1 ]; then
        echo "Differences found."
    else
        echo "Diff failed with exit code $diff_exit_code"
    fi

    return $diff_exit_code
}

print_translation_note() {
    echo "Translation note: locale/ is excluded from rsync to preserve Rosetta edits on the server."
    echo "If new translatable strings were deployed, run on the server:"
    echo "  python manage.py makemessages -a --no-wrap"
    echo "  python manage.py compilemessages"
    echo "Back up locale/*.po and locale/*.mo from the server into this repo and push them to GitHub."
}

print_usage() {
    echo "Usage: ./upload.sh [command]"
    echo
    echo "Commands:"
    echo "  (no command)            Dry-run sync to dev site"
    echo "  dryrun-dev              Dry-run sync to dev site"
    echo "  dryrun-test             Dry-run sync to test site"
    echo "  dryrun-test-safe        Dry-run safe sync to test site (skip newer remote files)"
    echo "  sync-dev                Sync code to dev site"
    echo "  sync-test               Sync code to test site"
    echo "  sync-test-safe          Sync code to test site (skip newer remote files)"
    echo "  dryrun-prod             Dry-run sync to prod site"
    echo "  sync-prod               Sync code to prod site"
    echo "  diff-dev <relative>     Diff local file against dev site file"
    echo "  diff-prod <relative>    Diff local file against prod site file"
    echo "  help | -h | --help      Show this help message"
}

if [ $# -eq 0 ]; then #execute a dry run to dev site
    rsync -avzn \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $DEVSITE
    echo "--------------------"
    echo "Performed dry run on on dev site $DEVSITE"
    echo "--------------------"
elif [ "$1" = 'dryrun-dev' ]; then #execute a dry run to dev site
    rsync -avzn \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $DEVSITE
    echo "--------------------"
    echo "Performed dry run on dev site $DEVSITE"
    echo "--------------------"
elif [ "$1" = 'dryrun-test' ]; then #execute a dry run to test site
    if [ -z "$TESTSITE" ]; then
        echo "TESTSITE must be set in $ENV_FILE for test commands"
        exit 1
    fi
    rsync -avzn \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $TESTSITE
    echo "--------------------"
    echo "Performed dry run on test site $TESTSITE"
    echo "--------------------"
elif [ "$1" = 'dryrun-test-safe' ]; then #execute a safe dry run to dev site
    if [ -z "$TESTSITE" ]; then
        echo "TESTSITE must be set in $ENV_FILE for test commands"
        exit 1
    fi
    rsync -avzn \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --update \
    --delete \
    $SOURCE $TESTSITE
    echo "--------------------"
    echo "Performed safe dry run on test site $TESTSITE (would skip newer remote files)"
    echo "--------------------"
elif [ "$1" = 'sync-dev' ]; then #push codes to devsite
    rsync -avz \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $DEVSITE
    echo "--------------------"
    echo "Performed sync code to dev site $DEVSITE"
    echo "--------------------"
    print_translation_note
elif [ "$1" = 'sync-test' ]; then #push code to test site
    if [ -z "$TESTSITE" ]; then
        echo "TESTSITE must be set in $ENV_FILE for test commands"
        exit 1
    fi
    rsync -avz \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $TESTSITE
    echo "--------------------"
    echo "Performed sync code to test site $TESTSITE"
    echo "--------------------"
    print_translation_note
elif [ "$1" = 'sync-test-safe' ]; then #push code to devsite, but never overwrite newer remote files
    if [ -z "$TESTSITE" ]; then
        echo "TESTSITE must be set in $ENV_FILE for test commands"
        exit 1
    fi
    rsync -avz \
    --checksum \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --update \
    --delete \
    $SOURCE $TESTSITE
    echo "--------------------"
    echo "Performed safe sync code to test site $TESTSITE (skipped newer remote files)"
    echo "--------------------"
    print_translation_note
elif [ $1 = 'dryrun-prod' ]; then #execute a dry run on production site
    rsync -avzn \
    --checksum \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $PRODSITE
    echo "--------------------"
    echo "Performed dry-run sync on prod site $PRODSITE"
    echo "--------------------"
elif [ $1 = 'sync-prod' ];then #push code to prod site
    rsync -avz \
    --checksum \
    --exclude-from=rsync-exclude.txt \
    --delete \
    $SOURCE $PRODSITE
    echo "--------------------"
    echo "Performed sync code to prod site $PRODSITE"
    echo "--------------------"
    print_translation_note
elif [ "$1" = 'diff-dev' ]; then
    diff_remote_file "$DEVSITE" "$2"
elif [ "$1" = 'diff-prod' ]; then
    diff_remote_file "$PRODSITE" "$2"
elif [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
    print_usage
else
    echo "arg not valid: $1"
    echo
    print_usage
    exit 1
fi
