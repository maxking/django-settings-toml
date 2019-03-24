from django_settings_toml import load_settings, update_settings


def test_update_settings_basic():
    # test that update settings actually sets the right attributes.
    update_settings('settings', {'KEY': 'Value'})
    # Now, let's import and see if the above value were set.
    import settings
    assert getattr(settings, 'KEY', None) is not None
    assert settings.KEY == 'Value'
    # Let's update one with multiple words joined with `_`.
    update_settings('settings', {'KEY': 'Value', 'KEY_ANOTHER_2': 'Value2'})
    assert getattr(settings, 'KEY_ANOTHER_2', None) is not None
    assert settings.KEY_ANOTHER_2 == 'Value2'


def test_update_settings_private():
    # test that private keys aren't set.
    update_settings('settings', {'_KEY': 'Value'})
    import settings
    assert getattr(settings, '_KEY', None) is None
    # Test that lowercase keys aren't set either.
    update_settings('settings', {'keys': 'value'})
    assert getattr(settings, '_KEY', None) is None


def test_template_substitution():
    # Test that values can have templates but won't raise errors if they can't
    # be substituted with a value.
    update_settings('settings', {'KEY1': 'Value-${KEY2}'})
    import settings
    assert getattr(settings, 'KEY1', None) is not None
    assert settings.KEY1 == 'Value-${KEY2}'
    # Now, test that values are substituted if they exist.
    update_settings('settings', {'KEY1': 'Value-${KEY2}', 'KEY2': '42'})
    assert settings.KEY1 == 'Value-42'


def test_update_settings_boolean(tmpdir):
    # Test that we can set boolean values for settings.
    p = tmpdir.mkdir('django-settings-toml1').join('example.toml')
    p.write("""\
VALUE = false
""")
    load_settings('settings', [str(p)])
    import settings
    assert getattr(settings, 'VALUE', None) is not None
    assert settings.VALUE is False


def test_update_settings_numerals(tmpdir):
    p = tmpdir.mkdir('django-settings-toml2').join('example.toml')
    p.write("""\
INT_VALUE = 100
""")
    load_settings('settings', [str(p)])
    import settings
    assert getattr(settings, 'INT_VALUE', None) is not None
    assert settings.INT_VALUE == 100


def test_update_settings_dictionary(tmpdir):
    # Test that we can load up Dictionaries.
    p = tmpdir.mkdir('django-settings-toml2').join('example.toml')
    p.write("""\
[LOGGING]
version = 1
disable_existing_loggers = false

[LOGGING.filters.require_debug_false]
'file' = 'django.utils.log.RequireDebugFalse'
""")
    load_settings('settings', [str(p)])
    import settings
    assert getattr(settings, 'LOGGING', None) is not None
    assert settings.LOGGING['version'] == 1
    assert settings.LOGGING['disable_existing_loggers'] is False
    assert settings.LOGGING['filters'] == { 'require_debug_false': {
        'file': 'django.utils.log.RequireDebugFalse'
    }}


def test_update_settings_dictionary_templates(tmpdir):
    # Test that we can load up Dictionaries.
    p = tmpdir.mkdir('django-settings-toml3').join('example.toml')
    p.write("""\
BASE_DIR = './tests'

[LOGGING]
version = 1
disable_existing_loggers = false
file = '${BASE_DIR}/example.log'
""")
    load_settings('settings', [str(p)])
    import settings
    assert getattr(settings, 'LOGGING', None) is not None
    assert settings.LOGGING['version'] == 1
    print(settings.LOGGING)
    assert settings.LOGGING['file'] == './tests/example.log'


def test_update_settings_dictionary_templates(tmpdir):
    # Test that we can load up Dictionaries.
    p = tmpdir.mkdir('django-settings-toml4').join('example.toml')
    p.write("""\
BASE_DIR_2 = './tests'

TEMPLATES = [
  'One',
  'Two',
  'Three',
  '${BASE_DIR_2}/Four',
]
""")
    load_settings('settings', [str(p)])
    import settings
    assert getattr(settings, 'TEMPLATES', None) is not None
    assert './tests/Four' in settings.TEMPLATES


def test_update_settings_uses_right_variable(tmpdir):
    # Test that variables defined in toml file overrides the one defined in the
    # settings itself for substition.
    p = tmpdir.mkdir('django-settings-toml5').join('example.toml')
    p.write("""\
BASE_DIR_TESTING = './tests'

VALUE = '${BASE_DIR_TESTING}/something'
""")
    load_settings('settings', [str(p)])
    import settings
    assert getattr(settings, 'VALUE', None) is not None
    assert settings.VALUE == './tests/something'
