

# Date & Time related imports
import time

import requests

from ArbitrageFinder.arbitrage_finder import ArbitrageFinder
from ArbitrageFinder.arbitrage_finderV2 import ArbitrageFinderV2

# Import oracles
from Oracle.cex_oracle import CexOracle
from Oracle.dex_oracle import DexOracle

from ProxyServer.proxy_server import ServerManager





def oracle_test(search_ticker: bool = True):

    arb = ArbitrageFinderV2()
    trending_tickers = arb.coin_oracle.get_trending_tickers()
    #trending_tickers = trending_tickers[:2]
    arb.find_arbitrage_routes(trending_tickers)  
    arb.write_top_routes(limit=1000)






if __name__ == "__main__":
    start = time.time()
    index = 0
    oracle_test(search_ticker=False)
    end = time.time()

    elapse = end - start
    print(f"[Elapse Time] {'{:.2f}'.format(elapse)} seconds")

