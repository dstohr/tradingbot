import requests
from autobahn.asyncio.wamp import ApplicationSession
import asyncio
from .util import HOST


class CoinsComponent(ApplicationSession):
    topic = 'ticker'
    async def onJoin(self, details):
        def on_event(*args):

            r = requests.post(
                "{}/{}".format(HOST, "tickers"),
                json={
                    "currencyPair": args[0],
                    "last": args[1],
                    "lowestAsk": args[2],
                    "highestBid": args[3],
                    "percentChange": args[4],
                    "baseVolume": args[5],
                    "quoteVolume": args[6],
                    "isFrozen": args[7],
                    "24hrHigh": args[8],
                    "24hrLow": args[9],
                }
            )
            print("Got event: {}, posted it with {}".format(args, r.status_code))

        await self.subscribe(on_event, self.topic)

    def onDisconnect(self):
        asyncio.get_event_loop().stop()
