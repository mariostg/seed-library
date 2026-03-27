#!/bin/sh
DEVSITE='mariost-gelais@mariostg.com:~/owsl.mariostg.com'
PRODSITE='mariost-gelais@mariostg.com:~/catalogue.wildflowerseedlibrary.ca'
SOURCE="/Users/mariost-gelais/Documents/gitprojects/owsl/djbp/*"

print_translation_note() {
    echo "Translation note: locale/ is excluded from rsync to preserve Rosetta edits on the server."
    echo "If new translatable strings were deployed, run on the server:"
    echo "  python manage.py makemessages -a"
    echo "  python manage.py compilemessages"
    echo "Back up locale/*.po and locale/*.mo from the server into this repo and push them to GitHub."
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
else
    echo "arg not valid"
fi
