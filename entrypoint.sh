#!/bin/bash
# shellcheck disable=SC1091

set -e 
source ./venv/bin/activate

python -m cli "$@"