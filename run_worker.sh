#!/usr/bin/env bash

set -e

main() {
    nice -n 19 celery -A k2var.tasks worker --loglevel=info
}

main
