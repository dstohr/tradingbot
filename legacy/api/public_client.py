import requests

from .util import API_HOST, ACCEPTABLE_CHART_PERIODS


class PoloniexPublicClient(object):
    @classmethod
    def _public_api_query(cls, command, data=None):
        data = {} if data is None else data
        data["command"] = command
        return requests.get(
            url="{}/{}".format(API_HOST, "public"),
            data=data,
        )

    @classmethod
    def return_ticker(cls):
        return cls._public_api_query({
            "command": "returnTicker"
        })

    @classmethod
    def return_24_volume(cls):
        return cls._public_api_query({
            "command": "return24Volume"
        })

    @classmethod
    def return_order_book(cls, currency_pair):
        return cls._public_api_query({
            "command": "returnOrderBook",
            "currencyPair": currency_pair,
        })

    # start, end Timestamp
    @classmethod
    def return_trade_history(cls, currency_pair, start, end):
        return cls._public_api_query({
            "command": "returnMarketTradeHistory",
            "currencyPair": currency_pair,
            "start": start,
            "end": end,
        })

    # start, end Timestamp
    @classmethod
    def return_chart_data(cls, currency_pair, start, end, period):
        assert period in ACCEPTABLE_CHART_PERIODS
        return cls._public_api_query({
            "command": "returnChartData",
            "currencyPair": currency_pair,
            "start": start,
            "end": end,
            "period": period,
        })

    @classmethod
    def return_currencies(cls):
        return cls._public_api_query({
            "command": "returnCurrencies",
        })

    @classmethod
    def return_load_orders(cls, currency):
        return cls._public_api_query({
            "command": "returnLoanOrders",
            "currency": currency,
        })
