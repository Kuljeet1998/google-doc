import sys
import os
import json

SECRETS_FILE = str('config/secrets.json')
if os.path.exists(SECRETS_FILE) is False:
    sys.exit(" Please add 'secrets.json' file in config/ folder.")

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    '''get the secret variable value of return exception'''
    try:
        return secrets[setting]
    except KeyError:
        error_message = 'Set the {0} environment variable'.format(setting)
        sys.exit(error_message)

TOKEN_FILE = str('config/token.json')
if os.path.exists(TOKEN_FILE) is False:
    sys.exit(" Please add 'token.json' file in config/ folder.")

with open(TOKEN_FILE) as f:
    tokens = json.loads(f.read())


def get_token(setting, tokens=tokens):
    '''get the token variable value of return exception'''
    try:
        return tokens[setting]
    except KeyError:
        error_message = 'Set the {0} environment variable'.format(setting)
        sys.exit(error_message)