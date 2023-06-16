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