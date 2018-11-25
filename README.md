## Active Campaign CLI

Virtualenv is required.

### Installation

```commandline
./install.sh 

# You need to give access to keychain for the python env.
codesign -f -s - .venv/bin/python

```
### Enable VirtualENV
```commandline
source .venv/bin/activate
```

### Call CLI
```commandline
./main.py or pytest
```