#!/bin/sh
if [ ! -f /data/splitwise.db ]; then
    python scripts/init_db.py
    python scripts/seed_db.py
fi
exec "$@"

