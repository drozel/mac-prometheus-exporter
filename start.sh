#!/bin/bash

cd "$(dirname "$0")"

. ./.venv/bin/activate
pip3 install -r requirements.txt
./mac-exporter.py
