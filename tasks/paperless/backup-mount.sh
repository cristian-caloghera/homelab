#!/bin/bash
#
# Script to mount an NFSv4 share idempotently.
# Running this script multiple times will not cause errors
# or multiple mounts if the share is already mounted.
#
# This script requires root privileges (e.g., run with sudo).

# --- Configuration ---
# Set your NFS server IP or hostname
NFS_SERVER="$1"

# Set the exported path on the NFS server
NFS_EXPORT="$2"

# Set the local directory where you want to mount the NFS share
MOUNT_POINT="$3"

# Set desired mount options (comma-separated)
# 'defaults' is usually a good start.
# Consider 'hard,intr' for better resilience to server issues.
# 'proto=tcp' is often preferred over UDP.
MOUNT_OPTIONS="defaults,hard,intr,proto=tcp"
# --- End Configuration ---

# --- Script Logic ---

# Ensure the script is run with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root."
   exit 1
fi

# Check if the local mount point directory exists. If not, create it.
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Mount point directory '$MOUNT_POINT' does not exist. Creating..."
    mkdir -p "$MOUNT_POINT"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create mount point directory '$MOUNT_POINT'."
        exit 1
    fi
fi

# Check if the share is already mounted using findmnt.
# findmnt returns 0 if the mount point is found, non-zero otherwise.
# We redirect output to /dev/null as we only care about the exit code.
if findmnt "$MOUNT_POINT" > /dev/null 2>&1; then
    echo "NFS share '$NFS_SERVER:$NFS_EXPORT' is already mounted at '$MOUNT_POINT'."
    # Exit successfully as the desired state (mounted) is already achieved.
    exit 0
else
    echo "Attempting to mount '$NFS_SERVER:$NFS_EXPORT' to '$MOUNT_POINT'..."
    # Attempt the mount operation
    mount -t nfs4 -o "$MOUNT_OPTIONS" "$NFS_SERVER:$NFS_EXPORT" "$MOUNT_POINT"

    # Check the exit status of the mount command
    if [ $? -eq 0 ]; then
        echo "Mount successful."
        exit 0
    else
        echo "Error: Mount failed."
        exit 1
    fi
fi

# --- End Script Logic ---
