FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Berlin"

RUN apt-get update && apt-get -y --no-install-recommends --no-install-suggests install \
    bash \
    mosquitto-clients \
    jq \
    curl \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /ha-mqtt-relay

COPY ha-mqtt-relay.sh /ha-mqtt-relay

ENTRYPOINT ["/usr/bin/bash", "/ha-mqtt-relay/ha-mqtt-relay.sh"]
