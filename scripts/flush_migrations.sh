find . -path "*/project/migrations/*.py" -not -name "__init__.py" -delete -print
find . -path "*/project/migrations/*.pyc"  -delete -print

if [ -f "db.sqlite3" ]; then
    mv "db.sqlite3" "db.sqlite3.bak"
else
    echo "No database file"
fi
