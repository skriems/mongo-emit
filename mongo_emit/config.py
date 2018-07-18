"""
config ingredients

custom config overwrites env vars which overwrite defaults
"""
import ast
import os
import sys

from yamlreader import yaml_load

from .cli import cli_args
from .helpers import utc_timestamp

# DEFAULT SETTINGS
DEBUG = False
MONGO = {
    'host': 'localhost',
    'port': 27017
}

STREAM = {
    'target':  'test.collection',
    'pipeline': [],
    'options': {}
}


def dump():
    for const in constants():
        print(const, getattr(sys.modules[__name__], const))


def constants():
    """ all uppercase constants in this module """
    module = sys.modules[__name__]
    return [key for key in dir(module) if key.isupper()]


def update(dct=None):
    """ get config from all possible sources
    1. config files
    2. env vars
    3. cli
    4. custom dict
    """
    update_from_files()
    update_from_env()
    update_from_cli()
    update_from_dict(dct or {})


def update_from_files():
    """ merge config files from all available env vars """
    dct = dict()
    for env_var in ('APP_SETTINGS_YAML', 'CONFIG_YAML', 'SECRETS_YAML'):
        if env_var in os.environ and os.path.exists(os.environ[env_var]):
            dct = yaml_load(os.environ[env_var], dct)

    # if start_at_operation_time is set in a config file, yamlreader converts
    # an iso8601 datetime string into a `datetime` opbject
    # We need to convert it to a `bson.timestamp.Timestamp`
    options = dct.get('stream', {}).get('options', {}) 
    date = options.get('start_at_operation_time')
    if date:
        dct['stream']['options']['start_at_operation_time'] = \
            utc_timestamp(date)
    update_from_dict(dct)


def update_from_env():
    """
    overwrite defaults with values from env variables. Note that only available
    configs get updated and no new env variables are added!

    Maps env vars splitted by underscores to nested config ingredients:
        MONGO_HOST -> MONGO['host']
        MONGO_PORT -> MONGO['port']
    """

    def _from_parts(parts, parent, value):
        for part in parts:
            part = part.lower()
            remains = parts[1:]

            # first element of the env var
            if isinstance(parent, str):
                parent = globals()[parent]

            if isinstance(parent, dict):
                if remains and isinstance(parent.get(part), dict):
                    _from_parts(remains, parent[part], value)
                elif isinstance(parent.get(part), list):
                    if isinstance(value, list):
                        parent[part].extend(value)
                    else:
                        parent[part].append(value)
                else:
                    parent[part] = value

    for env_var in os.environ:
        for const in constants():
            if env_var.startswith(const):
                parts = env_var.split('_')

                try:
                    value = ast.literal_eval(os.getenv(env_var))
                except ValueError:
                    # ast.literal_eval('string'), simply use the str
                    value = os.getenv(env_var)

                if len(parts) > 1:
                    _from_parts(parts[1:], parts[0], value)
                else:
                    globals()[env_var] = value


def update_from_dict(dct, parent=None):
    """ update this modules' constants from a dict """
    consts = constants()

    for key, value in dct.items():
        if key.upper() in consts:
            if isinstance(value, dict):
                update_from_dict(value, parent or globals()[key.upper()])
            else:
                if not isinstance(value, int):
                    try:
                        value = ast.literal_eval(value)
                    except ValueError:
                        # ast.literal_eval('string'); simply use the str
                        pass
                globals()[key.upper()] = value

        elif parent and key in parent and isinstance(value, dict):
            update_from_dict(value, parent[key])

        elif parent is not None:
            if not isinstance(value, int):
                try:
                    value = ast.literal_eval(value)
                except ValueError:
                    # value could be just a string or datetime
                    pass
            parent[key] = value


def update_from_cli():
    cli_options = {
        k: v
        for k, v in cli_args().__dict__.items()
        if v is not None
    }
    update_from_dict(dict(stream=cli_options))
