#!/usr/bin/env sh

# Default metric value to 0 (no reboot required)
REBOOT_REQUIRED=0

# Get the installed kernel version
INSTALLED_KERNEL=$(freebsd-version -k 2>&1)
EXIT_STATUS_INSTALLED=$?

# Get the running kernel version
RUNNING_KERNEL=$(uname -r 2>&1)
EXIT_STATUS_RUNNING=$?

# Check if both commands executed successfully
if [ ${EXIT_STATUS_INSTALLED} -ne 0 ] || [ ${EXIT_STATUS_RUNNING} -ne 0 ]; then
  echo "Error: Could not retrieve kernel versions." >&2
  if [ ${EXIT_STATUS_INSTALLED} -ne 0 ]; then
    echo "freebsd-version -k failed with exit status ${EXIT_STATUS_INSTALLED}. Output: ${INSTALLED_KERNEL}" >&2
  fi
  if [ ${EXIT_STATUS_RUNNING} -ne 0 ]; then
    echo "uname -r failed with exit status ${EXIT_STATUS_RUNNING}. Output: ${RUNNING_KERNEL}" >&2
  fi
  # In case of error, we cannot reliably determine the reboot status.
  exit 1 # Indicate failure
fi

# Compare the outputs
if [ "${INSTALLED_KERNEL}" = "${RUNNING_KERNEL}" ]; then
  echo "# Kernel versions match: Installed (${INSTALLED_KERNEL}) and Running (${RUNNING_KERNEL}) are the same."
  REBOOT_REQUIRED=0
else
  echo "Kernel versions differ: Installed (${INSTALLED_KERNEL}), Running (${RUNNING_KERNEL}). A reboot is likely required."
  REBOOT_REQUIRED=1
fi

# Define the Prometheus metric details
METRIC_NAME="node_reboot_required"
METRIC_HELP="Gauge indicating if a FreeBSD kernel update requires a system reboot (1=reboot required, 0=no reboot required)."
METRIC_TYPE="gauge"

# Print the Prometheus metric in text format to standard output.
echo "# HELP ${METRIC_NAME} ${METRIC_HELP}"
echo "# TYPE ${METRIC_NAME} ${METRIC_TYPE}"
echo "${METRIC_NAME} ${REBOOT_REQUIRED}"

# Define the Prometheus metric details for pending freebsd-update install
PENDING_INSTALL_METRIC_NAME="freebsd_update_pending_install"
PENDING_INSTALL_METRIC_HELP="Gauge indicating if freebsd-update has downloaded updates ready for installation (1=pending install, 0=no pending install)."
PENDING_INSTALL_METRIC_TYPE="gauge"

# Default metric value to 0 (no pending install)
PENDING_INSTALL=0

freebsd-update updatesready > /dev/null 2>&1
EXIT_STATUS_UPDATESREADY=$?

# Check the exit status of freebsd-update updatesready
if [ ${EXIT_STATUS_UPDATESREADY} -eq 2 ]; then
  # Exit status 2 means no updates are ready to be installed.
  PENDING_INSTALL=0
elif [ ${EXIT_STATUS_UPDATESREADY} -eq 0 ]; then
   PENDING_INSTALL=1
else
  echo "Warning: freebsd-update updatesready returned unexpected exit status ${EXIT_STATUS_UPDATESREADY}." >&2 # Log to stderr
  exit 2
fi

# Pending freebsd-update Install Metric
echo "# HELP ${PENDING_INSTALL_METRIC_NAME} ${PENDING_INSTALL_METRIC_HELP}"
echo "# TYPE ${PENDING_INSTALL_METRIC_NAME} ${PENDING_INSTALL_METRIC_TYPE}"
echo "${PENDING_INSTALL_METRIC_NAME} ${PENDING_INSTALL}"
