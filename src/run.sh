#!/bin/bash

cd "$(dirname $0)/jiwave" || exit 1

"../../.venv/bin/python3" -B -O "main.py"
