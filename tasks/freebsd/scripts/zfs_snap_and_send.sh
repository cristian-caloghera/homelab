#!/usr/bin/env sh

DATASET=$1
PREFIX=""

if [ -z "$DATASET" ]; then
	echo "Missing dataset argument!"
	echo
	echo "Usage $0 <data/set/to/snap/and/replicate> <destination>"
	exit 0
fi

DEST=$2

FIRST_SNAPSHOT=$(zfs list -t snapshot -o name -S creation 2>/dev/null | grep "$DATASET@$PREFIX" | tail -n 1)
LAST_SNAPSHOT=$(zfs list -t snapshot -o name -s creation 2>/dev/null | grep "$DATASET@$PREFIX" | tail -n 1)

echo "First snapshot: " $FIRST_SNAPSHOT
echo "Last snapshot : " $LAST_SNAPSHOT

FIRST_N=${FIRST_SNAPSHOT##*@$PREFIX}
LAST_N=${LAST_SNAPSHOT##*@$PREFIX}

INC_PARAM=""
N=0

# in case there was some snapshot LAST_N already there, increment from there
if [ -n "$LAST_N" ]; then
	N=$((LAST_N + 1))
	INC_PARAM="-i $DATASET@$PREFIX$LAST_N"
fi

SNAP_NOW=$DATASET@$PREFIX$N
zfs snapshot -r $SNAP_NOW
# we should actually check that destination exists
zfs send -R $INC_PARAM $SNAP_NOW | ssh root@becap zfs recv $DEST

echo you have now $((N - FIRST_N + 1)) snapshots
