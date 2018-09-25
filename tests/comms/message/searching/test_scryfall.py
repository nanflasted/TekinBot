import re
from unittest import mock

import pytest

import tekinbot.comms.message.searching.scryfall
from tekinbot.utils.config import tekin_id


mock_tmpl = 'tekinbot.comms.message.searching.scryfall.{}'
link_stem = 'https://api.scryfall.com/cards/named?{}={}'


class TestYoutube(object):

    @pytest.yield_fixture
    def mock_requests(self):
        with mock.patch(
            mock_tmpl.format('requests.get'),
        ) as mock_requests:
            type(mock_requests.return_value).ok = mock.PropertyMock(
                return_value=True)
            yield mock_requests

    @pytest.mark.parametrize('text, match', [
        (f'{tekin_id} mtg', False),
        (f'{tekin_id} mtg me something', True),
        (f'{tekin_id} mtg something', True),
        (f'{tekin_id} mtg: something', True),
        (f'{tekin_id} mtg:something', True),
        (f'{tekin_id} mtg exactly: something', True),
        (f'[[something]]', True),
        (f'something [[something]] else', True),
    ])
    def test_comm_re(self, text, match):
        assert bool(re.fullmatch(
            tekinbot.comms.message.searching.scryfall.comm_re,
            text
        )) == match

    @pytest.mark.parametrize('text, query, exact', [
        (f'{tekin_id} mtg me something', 'something', False),
        (f'{tekin_id} mtg me exactly something', 'something', True),
        (f'[[!something]]', 'something', True),
        (f'some [[!something]] thing else', 'something', True),
        (f'some [[something]] thing else', 'something', False),
    ])
    def test_process(
        self, text, query, exact,
        mock_requests,
    ):
        req = {'event': {'text': text}}
        tekinbot.comms.message.searching.scryfall.process(req)
        assert mock_requests.called
        assert len(mock_requests.call_args) == 2
        assert (
            ("exact" in mock_requests.call_args[1]['params']) == exact
        )
        assert ("something" in mock_requests.call_args[1]['params'].values())
