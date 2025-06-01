#!/bin/bash

# --- Configuration ---
#FTP_HOST="..."
#FTP_DIRECTORY="..."
#FTP_USER="..."
#FTP_PASS="..."
#LOCAL_DOWNLOAD_DIR="..."
#INTERVAL="..."

# --- Script ---

#echo "Attempting to process files from ftp://${FTP_HOST}${FTP_DIRECTORY} using lftp"
#echo "Assuming a FLAT directory structure and using 'get' for downloads."

#echo "Getting list of remote files in the flat directory ${FTP_DIRECTORY}..."

die_func()
{
    exit 0
}
trap die_func TERM

while true
do
	REMOTE_FILES_LIST=$(lftp -c "set ftp:ssl-allow no; open ${FTP_HOST}; user ${FTP_USER} ${FTP_PASS}; cd ${FTP_DIRECTORY}; nlist -1; bye" 2>&1)
	NLIST_STATUS=$?

	if [ $NLIST_STATUS -ne 0 ]; then
	    echo "Error getting the list of remote files using 'nlist -1'."
	    echo "Output from lftp nlist command:"
	    echo "$REMOTE_FILES_LIST"
	    echo "Cannot proceed. Exiting."
	    exit 1
	fi

	FILTERED_FILES=()
	while IFS= read -r line; do
	    if [ -n "$line" ]; then
	        FILTERED_FILES+=("$line")
	    fi
	done <<< "$REMOTE_FILES_LIST"

	#echo "Starting individual file downloads..."

	# Build the download command string with multiple 'get' commands
	LFTP_DOWNLOAD_COMMAND="set ftp:ssl-allow no; "
	LFTP_DOWNLOAD_COMMAND+="open -u ${FTP_USER},${FTP_PASS} ${FTP_HOST}; "
	# Change to remote dir AND specify local download dir using lcd
	LFTP_DOWNLOAD_COMMAND+="cd ${FTP_DIRECTORY}; lcd \"${LOCAL_DOWNLOAD_DIR}\"; "

	# Add a 'get' command for each file in the list
	for remote_file_to_get in "${FILTERED_FILES[@]}"; do
	    # Escape double quotes within the filename for the lftp command string
	    quoted_file=$(echo "$remote_file_to_get" | sed 's/"/\\"/g')
	    # Use 'get' with the quoted filename. Remove || echo to make session exit non-zero on failure.
	    LFTP_DOWNLOAD_COMMAND+="get \"$quoted_file\"; "
	    LFTP_DOWNLOAD_COMMAND+="rm \"$quoted_file\" || echo \"Error deleting $quoted_file\"; "
	done

	LFTP_DOWNLOAD_COMMAND+="bye"

	# Execute the lftp download command batch
	# Capture stderr to see potential individual get errors
	DOWNLOAD_OUTPUT=$(lftp -c "$LFTP_DOWNLOAD_COMMAND" 2>&1)
	DOWNLOAD_STATUS=$?

	if [ $DOWNLOAD_STATUS -ne 0 ]; then
	    echo "Download attempt finished. Review output for individual file errors."
	    echo "$DOWNLOAD_OUTPUT"
	fi

    sleep "$INTERVAL" &
    wait
    
	if [ $? -ne 0 ]; then
	    exit 1
	fi
done
