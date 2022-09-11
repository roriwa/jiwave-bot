#!/bin/bash

# change cd to repo-root
cd "$(dirname "$0")/.." || exit 1

# create venv if not already done
if [[ ! -f .venv ]]
then
  python3 -m venv .venv
fi

# install/upgrade packages
.venv/bin/pip -q install -U pip
.venv/bin/pip -q install -r requirements.txt

echo ""
echo "Project should be ready"
