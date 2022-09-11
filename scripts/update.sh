#!/bin/bash

cd "$(dirname "$0")/.." || exit 1

git pull -q || exit 1

bash scripts/install.sh
