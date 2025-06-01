#!/bin/sh

LOGS_DIR=/var/log/scrubber

mkdir -p $LOGS_DIR

# get a list of pool names and scrub each one
zpool list -H -o name |
while read -r name; do
  zpool scrub -w $name
  zpool status > $LOGS_DIR/$name.log
done
