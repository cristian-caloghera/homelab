#!/usr/bin/env sh

set -e

# in this PoC we ignore error handling

# power port mapping for reference:
# A1 - 1
# ...
# A6 - 6
# B1 - 7
# ...
# B6 - 12

# power on becap port
echo $(date -R):  "Power on becap port"
#mosquitto_pub -h norishor -t "power/cmd" -m '{"type": "cli", "cmd": "port 3 state set 1", "id": 0}'
ssh -i /root/.ssh/id_rsa_homelab_legacy_key admin@power port 3 state set ON

target=becap

echo $(date -R):  "Waiting for a successful ping..."
while true; do
  if ping -c 1 "$target" > /dev/null 2>&1; then
    echo $(date -R):  "Successfully pinged, can continue."
    break
  else
    echo $(date -R):  "Ping to $target failed. Retrying in 10 seconds..."
    sleep 10s
  fi
done

# ssh into becap and do a waiting scrub
echo $(date -R):  "SSH into becap and run a waiting scrub"
ssh root@"$target" /root/scripts/scrubber.sh

# since we are here not so often let's also do these 
/root/scripts/node_exporter_textfile_metric.sh /root/scripts/zfs_zpool.sh /var/tmp/node_exporter
/root/scripts/node_exporter_textfile_metric.sh /root/scripts/smartmon.sh /var/tmp/node_exporter
/root/scripts/node_exporter_textfile_metric.sh /root/scripts/freebsd_update_info.sh /var/tmp/node_exporter

echo $(date -R):  "Wait a bit to cool down"
sleep 30s

/root/scripts/zfs_snap_and_send.sh data/appdata becap/depozit/data/appdata

echo $(date -R):  "Wait a bit to cool down"
sleep 30s

# ssh into becap and issue a poweroff
echo $(date -R):  "Powering off"
ssh root@becap poweroff

echo $(date -R):  "Waiting for $target to become unreachable..."

while true; do
  if ! ping -c 1 "$target" > /dev/null 2>&1; then
    echo $(date -R):  "$target is no longer reachable!"
    break
  else
    echo $(date -R):  "$target is still reachable. Checking again in 10 seconds..."
    sleep 10
  fi
done

# power cut on becap port
echo $(date -R):  "Wait 60s then cut the power"
sleep 60s
ssh -i /root/.ssh/id_rsa_homelab_legacy_key admin@power port 3 state set OFF
