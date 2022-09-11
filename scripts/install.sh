#!/bin/bash

# change cd to repo-root
cd "$(dirname "$0")/.." || exit 1

# create venv if not already done
if [[ ! -d .venv ]]
then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# install/upgrade packages
echo "Updating/Installing dependencies..."
.venv/bin/pip -q install -U pip
.venv/bin/pip -q install -r requirements.txt

if [[ ! -f /etc/systemd/system/jiwave-bot.service ]]
then
  echo ""
  echo "WARN: Recommended way of running this bot (as service) seems not configured"
fi

echo ""
echo "Project should be ready"
