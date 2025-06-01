#!/usr/bin/env bash

# do the local backup becuase of bullshit path handling in Paperless
docker exec paperless-webserver document_exporter ../export --zip

TMP_EXPORT_DIR=/opt/stacks/paperless/export
BACKUP_DIR=/mnt/data/paperless-exports

cp $TMP_EXPORT_DIR/* $BACKUP_DIR
rm $TMP_EXPORT_DIR/*

# Delete older backups but keep at leas 3 around
# list directories, only names, sorted by change time, most recent first
# list from line 4 (i.e. skip first 3 lines)
# delete the rest

ls -1tc $BACKUP_DIR | tail -n +4 | xargs -I {} --no-run-if-empty rm -r $BACKUP_DIR/{}
