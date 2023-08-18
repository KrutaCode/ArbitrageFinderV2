

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
    address = "0xdC6fF44d5d932Cbd77B52E5612Ba0529DC6226F1"
    #address = "0x514910771af9ca656af840dff83e8264ecf986ca"
    #arb = ArbitrageFinder()
   
    #trending_tickers = ["pepe", ""]
    #arbitrage_canidates = arb.find_arbitrage_mixed(trending_tickers, search_ticker)
    #arb.display_arbitrage(arbitrage_canidates)
    #arb.coin_oracle.get_coinname_by_address(address, network="optimism")
    arb = ArbitrageFinderV2()
    trending_tickers = arb.coin_oracle.get_trending_tickers()
    trending_tickers = trending_tickers[:2]
    arb.find_arbitrage_routes(trending_tickers)  






if __name__ == "__main__":
    start = time.time()
    index = 0
    oracle_test(search_ticker=False)
    end = time.time()

    elapse = end - start
    print(f"[Elapse Time] {'{:.2f}'.format(elapse)} seconds")

