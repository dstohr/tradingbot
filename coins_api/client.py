from .util import HOST, LIMIT
import requests
import json


class CoinsApi(object):
    @classmethod
    def get_candlesticks(cls, base_coin, destination_coin, start_date, end_date, extra_filter=None):
        mongo_filter = extra_filter or {}
        mongo_filter["baseCoin"] = base_coin
        mongo_filter["destinationCoin"] = destination_coin
        mongo_filter["dateTimestamp"] = {"$gt": start_date.timestamp(), "$lt": end_date.timestamp()}
        return cls.get_all("{}/{}?filter={}".format(HOST, "candlesticks", json.dumps(mongo_filter).replace(" ", "")))

    @classmethod
    def get_page(cls, url, page_number):
        url = "{}&limit={}&skip={}".format(url, LIMIT, LIMIT*page_number)
        response = requests.get(url)
        print(url)
        if not response.ok:
            raise Exception("Response from api: {}, {}".format(response.status_code, response.text))
        return response.text

    @classmethod
    def get_all(cls, url):
        page_number = 0
        while True:
            items = json.loads(cls.get_page(url, page_number))
            page_number += 1
            if items["count"] == 0:
                break
            yield items["data"]
