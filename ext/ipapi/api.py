import requests
from typing import NamedTuple


BASE_URL = "http://ip-api.com/json"


class Err(Exception): pass  # noqa
class TimeoutErr(Err): pass  # noqa


class Response(NamedTuple):
    country_code: str


class API(object):

    def query(self, ip: str) -> Response:
        url = f'{BASE_URL}/{ip}'
        params = {
            'fields': 'countryCode',
        }
        try:
            resp = requests.get(url, params=params)
        except requests.Timeout:
            raise TimeoutErr()
        if resp.status_code != 200:
            raise Err()
        data = resp.json()
        return Response(
            country_code=(data.get('countryCode', '') or ''),
        )
