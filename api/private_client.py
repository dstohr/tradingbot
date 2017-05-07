import hashlib
import hmac
import json
import time
import urllib.parse

import requests

from .util import API_HOST


class PoloniexPrivateClient(object):
    def __init__(self, key=None, secret=None):
        self._key = key
        self._secret = secret

    def _private_api_query(self, command, data=None):
        assert self._key is not None and self._secret is not None
        data = {} if data is None else data
        data["command"] = command
        data["nonce"] = int(time.time() * 1000)
        sign = hmac.new(self._secret, urllib.parse.urlencode(data), hashlib.sha512).hexdigest()
        headers = {
            'Sign': sign,
            'Key': self._key,
        }
        return json.loads(requests.post(
            url="{}/{}".format(API_HOST, "tradingApi"),
            data=data,
            headers=headers,
        ))