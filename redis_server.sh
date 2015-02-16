#!/usr/bin/env bash
set -e

main() {
    redis-server config/redis.conf
}

main
