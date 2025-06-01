#!/usr/bin/env bash

# this script should run inside the influx Docker image:
# docker exec -i influxdb2 bash < all-access-token.sh

# Wait for InfluxDB to be up and running
until influx ping 1> /dev/null
do
  2&>1 echo "Waiting for InfluxDB to start..."
  sleep 1
done

# Extract admin token
ADMIN_TOKEN=$(cat /run/secrets/influxdb2-admin-token)

ID_COUNT=$(influx auth list --hide-headers --token $ADMIN_TOKEN | wc -l)

if (( ID_COUNT == 1 )); then
  # looks like only the admin token is there
  # so we need an all-access token for applications to use
  influx auth create --hide-headers --all-access --org BuruOrg --token $ADMIN_TOKEN | tr -s "\t" | cut -f 2 | tr -d "\n"
fi

if (( ID_COUNT == 2 )); then
  # looks like next to the admin token there's also another one already created
  # we consider this one the all-access token
  # get all ids                                        | list non-admin token | print field token only| remove newline
  influx auth list --hide-headers --token $ADMIN_TOKEN | grep -v $ADMIN_TOKEN | tr -s "\t" | cut -f 2 | tr -d "\n"
fi

# if we get here it means ID_COUNT > 2 and there are multiple tokens
# in this case we do nothing
