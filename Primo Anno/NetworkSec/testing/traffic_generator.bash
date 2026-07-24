#!/usr/bin/env bash

CURL="$(brew --prefix curl)/bin/curl"

TOTAL_REQUESTS=10
CONCURRENCY=2
URL="https://127.0.0.1:4433/"

seq 1 "$TOTAL_REQUESTS" | xargs -P "$CONCURRENCY" -I{} \
  "$CURL" \
    --http3-only \
    -k \
    -s \
    -o /dev/null \
    -w "request={} status=%{http_code} time=%{time_total}\n" \
    "$URL"