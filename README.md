## Active Campaign CLI

Virtualenv is required.

### Installation

```commandline
./install.sh 

# You need to give access to keychain for the python env.
codesign -f -s - .venv/bin/python
python -m keyring set active_campaign token

# Verify Token
python -m keyring get active_campaign token

```
### Enable VirtualENV
```commandline
source .venv/bin/activate
```

### Call CLI
```commandline
./main.py or pytest
```
