#!/usr/bin/env bash

set -e
source ../.venv/bin/activate

python3 run.py "$1"
# sleep 5
# python3 -V
