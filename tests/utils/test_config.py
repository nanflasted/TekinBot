from unittest import mock

import pytest

from tekinbot.utils.config import tekin_secrets


class TestTekinSecrets(object):

    @pytest.yield_fixture
    def mock_config(self):
        fake_config = {'testy': 'mctestface',
                       'you': {'should_take': 'eecs_132'}}
        with mock.patch(
            'tekinbot.utils.config.tekin_secret_dict',
            return_value=fake_config,
        ) as mock_config:
            yield mock_config

    @pytest.mark.parametrize(
        'key_name, expected', [
            ('testy', 'mctestface'),
            ('you.should_take', 'eecs_132'),
        ])
    def test_tekin_secrets__normal(self, key_name, expected, mock_config):
        assert tekin_secrets(key_name) == expected

    def test_tekin_secrets__invalid_key(self, mock_config):
        with pytest.raises(KeyError):
            tekin_secrets('you_shouldntake')
