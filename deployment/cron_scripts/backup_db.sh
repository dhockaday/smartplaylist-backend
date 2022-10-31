#!/bin/bash

NOW=$(date '+%Y-%m-%d-%H%M%S')
FILENAME="-smartplaylist-backup.psql"

echo $NOW "Running backup"

time docker exec db pg_dump -U postgres -w -F c spotify -f /pg_backup/$NOW$FILENAME

NOW=$(date '+%Y-%m-%d-%H%M%S')
echo $NOW "Finished backup"
