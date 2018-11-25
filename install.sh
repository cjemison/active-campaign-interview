#!/usr/bin/env bash

if [[ -d ".venv" ]]; then
  rm -rf .venv
fi

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# included for mac sierra
# codesign -f -s - .venv/bin/python

# codesign -dvvvv .venv/bin/python