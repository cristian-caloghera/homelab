#!/usr/bin/env bash

# this script should run inside the influx Docker image:
# docker exec -i influxdb2 bash < backup.sh

# Extract admin token
TOKEN=$(cat /run/secrets/influxdb2-admin-token)
#docker exec influxdb2 ls -l /var/lib

BACKUP_DIR=/var/lib/influxdb2-backup

# Do the backup
influx backup \
  $BACKUP_DIR/backup_$(date '+%Y-%m-%d_%H-%M') \
  --token $TOKEN

# Delete older backups but keep at leas 3 around
# list directories, only names, sorted by change time, most recent first
# list from line 4 (i.e. skip first 3 lines)
# delete the rest

ls -d1tc $BACKUP_DIR/* | tail -n +4 | xargs --no-run-if-empty rm -r
