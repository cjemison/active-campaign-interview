#!/usr/bin/env bash

if [[ -d ".venv" ]]; then
  rm -rf .venv
fi

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m keyring set active_campaign token


# included for mac sierra
# codesign -f -s - .venv/bin/python
# python -m keyring set active_campaign token
# python -m keyring get active_campaign token

# codesign -dvvvv .venv/bin/python