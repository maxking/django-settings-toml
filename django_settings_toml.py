import sys
import toml

from pathlib import Path
from string import Template


def update_settings(module_name, extra_settings):
    try:
        module = sys.modules[module_name]
    except KeyError:
        __import__(module_name)
        module = sys.modules[module_name]

    for (member, value) in extra_settings.items():
        if member.isupper() and not member.startswith('_'):
            value = Template(value).safe_substitute(**extra_settings)
            setattr(module, member, value)


def load_settings(module_name, settings_paths):
    """Export dictionary variables and properties to module namespace.

    This will export keys that are all upper case and doesn't begin with
    ``_``. These members will be set as attributes on the module
    ``module_name``.

    :param module_name: Name of the module to be used as Django's settings
        module.
    :param settings_paths: A list of file paths to look for settings. The
        first one found is read.
    """
    for path in settings_paths:
        if Path(path).exists():
            settings_path = path
            break
    else:
        print('Error: None of the config files exist.')
        return

    with open(settings_path) as fd:
        try:
            update_settings(
                module_name, toml.load(fd))
        except toml.decoder.TomlDecodeError as error:
            print('Invalid TOML configuration file: {}'.format(settings_path))
            print(error)
            return
