#!/usr/bin/env bash
set -ex

docker build -t spoa.dev:latest .

docker run \
        -it --rm -d --name spoa \
        --expose 9008 \
        spoa.dev:latest