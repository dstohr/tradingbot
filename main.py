from api.push_client import PoloniexApplicationRunner
from coins_api.push_component import CoinsComponent


a = PoloniexApplicationRunner(CoinsComponent)
a.run_ticker()
