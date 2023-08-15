

# Date & Time related imports
import time

import requests

from ArbitrageFinder.arbitrage_finder import ArbitrageFinder

# Import oracles
from Oracle.cex_oracle import CexOracle
from Oracle.dex_oracle import DexOracle

from ProxyServer.proxy_server import ServerManager





def oracle_test(search_ticker: bool = True):
    arb = ArbitrageFinder()
    trending_tickers = arb.coin_oracle.get_trending_tickers()
    arbitrage_canidates = arb.find_arbitrage_mixed(trending_tickers, search_ticker)
    arb.display_arbitrage(arbitrage_canidates)


if __name__ == "__main__":
    start = time.time()
    index = 0
    oracle_test(search_ticker=False)
    end = time.time()

    elapse = end - start
    print(f"[Elapse Time] {'{:.2f}'.format(elapse)} seconds")

