import asyncio

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

from .util import WS_HOST


class BasicComponent(ApplicationSession):
    topic = 'ticker'
    async def onJoin(self, details):
        def on_event(*args):
            print("Got event: {}".format(args))

        await self.subscribe(on_event, self.topic)

    def onDisconnect(self):
        asyncio.get_event_loop().stop()


class PoloniexApplicationRunner(ApplicationRunner):
    ComponentClass = None

    def __init__(self, ComponentClass=BasicComponent):
        self.ComponentClass = ComponentClass
        super(PoloniexApplicationRunner, self).__init__(
            WS_HOST,
            realm="realm1",
        )

    def run_ticker(self):
        self.run(self.ComponentClass)
