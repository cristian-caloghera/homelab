FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Berlin"

RUN apt-get update && apt-get -y --no-install-recommends --no-install-suggests install \
    bash \
    mosquitto-clients \
    jq \
    curl \
    openssh-client \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /user-notify

COPY user-notify.sh notify-d.sh /user-notify

ENTRYPOINT ["/usr/bin/bash", "/user-notify/user-notify.sh"]
