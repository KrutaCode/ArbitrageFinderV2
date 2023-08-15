
# Date * Time realted imports
import time 
import datetime as dt

# Requests related imports 
import requests


# CCXT related imports.
import ccxt
from ccxt.base.errors import BadSymbol, RateLimitExceeded

# Asynchronous related imports
import asyncio
import concurrent.futures


class CexOracle:
    def __init__(self, data_source: str = "", cex_list: list = [], ticker_list: list = [], market: str = "USDT") -> None:
        
    
        self.cex_list = cex_list
        self.ticker_list = ticker_list
        self.market = market
        self.cex_objects = [getattr(ccxt, cex_name.lower())() for cex_name in self.cex_list]
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------  Thread Operations  -----------------------------------'''
    '''-----------------------------------'''
    def get_prices_thread(self):
        results = []
        index = 1
        with concurrent.futures.ThreadPoolExecutor() as thread_executor:
            for cex in self.cex_objects:
                for ticker in self.ticker_list:
                    future = thread_executor.submit(self.thread_fetch_ticker, cex, ticker)
                    future_data = {
                        "exchange": cex.id,
                        "ticker": ticker,
                        "data": future
                    }
                    #print(f"Future: {future_data}")
                    results.append(future_data)
                    index += 1
        
        # Results.
        #print(f"Results: {results}")
        ticker_data = []
        for fut in results:
            exchange_name = fut["exchange"]
            ticker = fut["ticker"]
            future_data = fut["data"].result()
            # Check if the future_data is not None. 
            if future_data is not None:
                data = {
                    "exchange": exchange_name,
                    "ticker": ticker,
                    "data": future_data
                }
                ticker_data.append(data)
        
        ticker_data = self.group_cex_data(ticker_data)
        return ticker_data
    '''-----------------------------------'''
    def thread_fetch_ticker(self, cex: ccxt, ticker: str):
        trade_pair = f"{ticker}/{self.market}"
        try:
            ticker = cex.fetch_ticker(trade_pair)
            return ticker
        except RateLimitExceeded as e:
            print(f"{e}")
        except BadSymbol as e:
            print(f"{e}")
        except Exception as e:
            print(f"{e}")

    '''-----------------------------------'''
    def group_cex_data(self, cex_data):
        grouped_data = {}

        for item in cex_data:
            ticker = item["ticker"]
            if ticker not in grouped_data:
                grouped_data[ticker] = []
           
            grouped_data[ticker].append({
                "exchange": item["exchange"],
                "ticker": ticker,
                "data": item["data"]
            })

        return grouped_data 

    '''-----------------------------------'''


    '''-----------------------------------  CoinGecko Operations  -----------------------------------'''
    '''-----------------------------------'''
    def get_exchange_prices(self, name: str):
        url = f"https://api.coingecko.com/api/v3/coins/{name.lower()}"
        response = requests.get(url)
        data = response.json()

        print(f"Data: {data['tickers']}")

        if 'platform' in data and self.network in data["platforms"]:
            print(f"Data: {data['platforms'][self.network]}")
        print(f"Data: {data['platforms'].keys()}")
        response = re
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''


        
