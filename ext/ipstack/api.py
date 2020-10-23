import requests
from typing import NamedTuple


BASE_URL = "http://api.ipstack.com/"


class Err(Exception): pass  # noqa
class TimeoutErr(Err): pass  # noqa


class Response(NamedTuple):
    ip: str
    country_code: str


class API(object):

    def __init__(self, token):
        self.token = token

    def lookup(self, ip: str) -> Response:
        url = f'{BASE_URL}/{ip}'
        params = {
            'access_key': self.token,
        }
        try:
            resp = requests.get(url, params=params)
        except requests.Timeout:
            raise TimeoutErr()
        if resp.status_code != 200:
            raise Err()
        data = resp.json()
        return Response(
            ip=data['ip'],
            country_code=data['country_code'] or '',
        )
