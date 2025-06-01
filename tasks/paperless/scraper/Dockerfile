FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/Berlin"

RUN mkdir /scraper && apt-get update && apt-get -y --no-install-recommends --no-install-suggests install \
    bash \
    lftp \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY scrape.sh /scraper/scrape.sh

ENTRYPOINT ["/usr/bin/bash", "/scraper/scrape.sh"]
