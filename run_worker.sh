#!/usr/bin/env bash

set -e

main() {
    celery -A k2var.tasks worker --loglevel=info
}

main
