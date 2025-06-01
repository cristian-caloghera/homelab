#!/bin/bash

# SIGTERM propagation
prep_term()
{
  unset term_child pid
  unset term_kill needed
  trap 'handle_term' TERM INT
}

handle_term()
{
  if [ "${term_child_pid}" ]; then
    kill -TERM "${term_child_pid}" 2>/dev/null
  else
    term_kill_needed="yes"
  fi
}

wait_term()
{
  #term_child_pid=$!
  if [ "${term_kill_needed}" ]; then
    kill -TERM "${term_child_pid}" 2>/dev/null
  fi
  wait ${term_child_pid} 2>/dev/null
  trap - TERM INT
  wait ${term_child_pid} 2>/dev/null
}

# Define MQTT broker and topics

# source
RELAY_FROM_SPLIT=(${RELAY_FROM_MQTT//:/ })
RELAY_FROM_ADDR=${RELAY_FROM_SPLIT[0]}
RELAY_FROM_PORT=${RELAY_FROM_SPLIT[1]:-1883}

declare -a TOPICS_ARRAY=("${TOPICS[@]}")

# Function to handle payloads

handle_payload()
{
  local topic=$1
  local payload=$2

  echo "Received payload on ${topic}:\n $payload"

  case "$topic" in
    "ems-esp/boiler_data_dhw")
      # add your action here
      local curtemp=$(echo ${payload} | jq ".curtemp")
      local ccujack_json="{\"v\": ${curtemp}}"
      echo ${curtemp} ${ccujack_json}
      curl -X PUT -d "${ccujack_json}" http://${CCU_JACK}/sysvar/13101/~pv
      ;;
    "topic2")
      # add your action here
      ;;
    "topic3")
      # add your action here
      ;;
    *)
      echo "Ignoring unknown topic: $topic"
  esac
}

# Build the mosquitto_sub command with multiple -t options
CMD="mosquitto_sub -h ${RELAY_FROM_ADDR} -p ${RELAY_FROM_PORT} -v"
while IFS= read -r T; do
  CMD+=" -t $T"
done <<< "$TOPICS"

echo "Subscribing to ${RELAY_FROM_ADDR}:${RELAY_FROM_PORT}"
echo "Executing: " $CMD
prep_term

tmp=$(mktemp -d)
mkfifo "$tmp/pipe"
$CMD > "$tmp/pipe" & term_child_pid=$!

while read -r topic payload; do
  handle_payload "$topic" "$payload"
done < "$tmp/pipe"

wait_term
