# This script ensures the Prometheus will not scrap an impartial
# metrics file. This is achieved by first dumping the generated
# metrics into a temporary file (*.$$) and then renaming this
# file to its proper name.

# Check the number of arguments
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 <script_to_execute.sh> [output_directory]"
    echo "  <script_to_execute.sh>: The script to execute."
    echo "  [output_directory]:     Optional. The directory to store output files. Defaults to current directory."
    exit 1
fi

SCRIPT_TO_RUN="$1"
# Set output directory, default to current directory if not provided
OUTPUT_DIR="${2:-.}"

# Construct the initial output file name using the script name and process ID
# Prepend the output directory path
OUTPUT_FILE_TEMP="${OUTPUT_DIR}/$(basename -- "$SCRIPT_TO_RUN").$$"

# Derive the final file name by removing .sh and adding .prom
# Prepend the output directory path
BASE_NAME=$(basename -- "$SCRIPT_TO_RUN")
# Remove .sh suffix if it exists
BASE_NAME_NO_SH="${BASE_NAME%.sh}"
# Add the .prom suffix
FINAL_FILE="${OUTPUT_DIR}/${BASE_NAME_NO_SH}.prom"

# --- Input Validation ---

# Check if the script to run exists and is executable
if [ ! -f "$SCRIPT_TO_RUN" ]; then
    echo "Error: Script to execute '$SCRIPT_TO_RUN' not found."
    exit 1
fi

# Check if the file has execute permissions
if [ ! -x "$SCRIPT_TO_RUN" ]; then
    echo "Error: Script to execute '$SCRIPT_TO_RUN' is not executable. Please add execute permission (e.g., chmod +x '$SCRIPT_TO_RUN')."
    exit 1
fi

# --- Directory Handling ---

# Create the output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Output directory '$OUTPUT_DIR' not found. Creating it..."
    if ! mkdir -p "$OUTPUT_DIR"; then
        echo "Error: Failed to create output directory '$OUTPUT_DIR'."
        exit 1
    fi
fi

# Check if the output directory is writable
if [ ! -w "$OUTPUT_DIR" ]; then
    echo "Error: Output directory '$OUTPUT_DIR' is not writable."
    exit 1
fi

# --- Execution and Capture ---

echo "Execute: '$SCRIPT_TO_RUN' to temporary file '$OUTPUT_FILE_TEMP'"
if "$SCRIPT_TO_RUN" > "$OUTPUT_FILE_TEMP" 2>&1; then
    echo "Execute: '$SCRIPT_TO_RUN' finished successfully."
else
    SCRIPT_EXIT_STATUS=$?
    echo "Error: Execution of '$SCRIPT_TO_RUN' failed with status $SCRIPT_EXIT_STATUS."
    exit 1
fi

# --- Renaming ---

# Rename the temporary output file to the final .prom name in the same directory
if mv "$OUTPUT_FILE_TEMP" "$FINAL_FILE"; then
    echo "Output successfully renamed to '$FINAL_FILE'."
else
    if [ -f "$OUTPUT_FILE_TEMP" ]; then
        echo "Attempting to remove temporary file '$OUTPUT_FILE_TEMP' due to renaming failure."
        rm "$OUTPUT_FILE_TEMP"
    fi
    echo "Error: Failed to rename '$OUTPUT_FILE_TEMP' to '$FINAL_FILE'."
    exit 1
fi
