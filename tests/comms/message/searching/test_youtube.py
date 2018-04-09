import re
from unittest import mock

import pytest

import tekinbot.comms.message.searching.youtube
from tekinbot.utils.config import tekin_id


mock_tmpl = 'tekinbot.comms.message.searching.youtube.{}'
res_stem = 'https://www.youtube.com/results'


class TestYoutube(object):

    @pytest.yield_fixture
    def mock_requests(self):
        with mock.patch(
            mock_tmpl.format('requests.get'),
        ) as mock_requests:
            type(mock_requests.return_value).ok = mock.PropertyMock(
                return_value=True)
            yield mock_requests

    @pytest.yield_fixture
    def mock_bs4(self):
        with mock.patch(
            mock_tmpl.format('BeautifulSoup')
        ) as mock_bs4, mock.patch(
            mock_tmpl.format('BeautifulSoup.Tag.get'),
            return_value='lel',
        ):
            yield mock_bs4

    @pytest.yield_fixture
    def mock_random(self):
        with mock.patch(
            mock_tmpl.format('random'),
        ) as mock_random:
            yield mock_random

    @pytest.mark.parametrize('text, match', [
        (f'{tekin_id} youtube', False),
        (f'{tekin_id} youtube me something', True),
        (f'{tekin_id} youtube something', True),
        (f'{tekin_id} youtube: something', True),
        (f'{tekin_id} youtube:something', True),
        (f'{tekin_id} youtube exactly: something', True),
    ])
    def test_comm_re(self, text, match):
        assert bool(re.fullmatch(
            tekinbot.comms.message.searching.youtube.comm_re,
            text
        )) == match

    @pytest.mark.parametrize('text, query, exact', [
        (f'{tekin_id} youtube me something', 'something', False),
        (f'{tekin_id} youtube me exactly something', 'something', True),
    ])
    def test_process(
        self, text, query, exact,
        mock_requests, mock_bs4, mock_random
    ):
        req = {'event': {'text': text}}
        with mock.patch(
            mock_tmpl.format('extract_search_res'),
            return_value=['testy', 'mc', 'testface'],
        ):
            tekinbot.comms.message.searching.youtube.process(req)
            payload = {'search_query': query.encode('utf-8')}
            mock_requests.assert_called_once_with(res_stem, params=payload)
            assert exact != mock_random.choice.called
