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
