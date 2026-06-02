#!/bin/sh
DEVSITE='mariost-gelais@mariostg.com:~/owsl.mariostg.com'
PRODSITE='mariost-gelais@mariostg.com:~/catalogue.wildflowerseedlibrary.ca'
SOURCE="/Users/mariost-gelais/Documents/gitprojects/owsl/djbp/*"
LOCALROOT="/Users/mariost-gelais/Documents/gitprojects/owsl/djbp"

diff_remote_file() {
    target_site="$1"
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

    tmp_remote_file=$(mktemp)
    if [ $? -ne 0 ]; then
        echo "Failed to create temp file"
        exit 1
    fi

    # Fetch remote file then compare using POSIX-compatible diff.
    ssh mariost-gelais@mariostg.com "cat $target_site/$relpath" > "$tmp_remote_file"
    if [ $? -ne 0 ]; then
        echo "Failed to read remote file: $target_site/$relpath"
        rm -f "$tmp_remote_file"
        exit 1
    fi

    diff -u "$local_file" "$tmp_remote_file"
    diff_exit_code=$?
    rm -f "$tmp_remote_file"
    return $diff_exit_code
}

print_translation_note() {
    echo "Translation note: locale/ is excluded from rsync to preserve Rosetta edits on the server."
    echo "If new translatable strings were deployed, run on the server:"
    echo "  python manage.py makemessages -a"
    echo "  python manage.py compilemessages"
    echo "Back up locale/*.po and locale/*.mo from the server into this repo and push them to GitHub."
}

print_usage() {
    echo "Usage: ./upload.sh [command]"
    echo
    echo "Commands:"
    echo "  (no command)            Dry-run sync to dev site"
    echo "  sync-test               Sync code to dev site"
    echo "  dryrun-prod             Dry-run sync to prod site"
    echo "  sync-prod               Sync code to prod site"
    echo "  diff-dev <relative>     Diff local file against dev site file"
    echo "  diff-prod <relative>    Diff local file against prod site file"
    echo "  help | -h | --help      Show this help message"
}

if [ $# -eq 0 ]; then #execute a dry run to dev site
    rsync -avzn \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --update \
    --delete \
    $SOURCE $DEVSITE
    echo "--------------------"
    echo "Performed dry run on on dev site $DEVSITE"
    echo "--------------------"
elif [ $1 = 'sync-test' ];then #push codes to devsite
    rsync -avz \
    --filter 'protect /media/*' \
    --exclude-from=rsync-exclude.txt \
    --update \
    --delete \
    $SOURCE $DEVSITE
    echo "--------------------"
    echo "Performed sync code to dev site $DEVSITE"
    echo "--------------------"
    print_translation_note
elif [ $1 = 'dryrun-prod' ]; then #execute a dry run on production site
    rsync -avzn \
    --exclude-from=rsync-exclude.txt \
    --update \
    --delete \
    $SOURCE $PRODSITE
    echo "--------------------"
    echo "Performed dry-run sync on prod site $PRODSITE"
    echo "--------------------"
elif [ $1 = 'sync-prod' ];then #push code to prod site
    rsync -avz \
    --exclude-from=rsync-exclude.txt \
    --update \
    --delete \
    $SOURCE $PRODSITE
    echo "--------------------"
    echo "Performed sync code to prod site $PRODSITE"
    echo "--------------------"
    print_translation_note
elif [ "$1" = 'diff-dev' ]; then
    diff_remote_file "~/owsl.mariostg.com" "$2"
elif [ "$1" = 'diff-prod' ]; then
    diff_remote_file "~/catalogue.wildflowerseedlibrary.ca" "$2"
elif [ "$1" = 'help' ] || [ "$1" = '-h' ] || [ "$1" = '--help' ]; then
    print_usage
else
    echo "arg not valid: $1"
    echo
    print_usage
    exit 1
fi
