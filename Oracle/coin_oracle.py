# Date * Time realted imports
import time 
import datetime as dt

# Requests related imports 
import requests

# Pandas related imports
import pandas as pd

from pycoingecko import CoinGeckoAPI


coin_id_path = "D:\\Coding\\VisualStudioCode\\Projects\\Python\\ArbitrageFinderV2\\CoinStorage\\cg_coin_id.csv"
coin_supply_path = "D:\\Coding\\VisualStudioCode\\Projects\\Python\\ArbitrageFinderV2\\CoinStorage\\cg_coin_supply.csv"


class CoinOracle:
    def __init__(self) -> None:

        self.coin_ids = pd.read_csv(coin_id_path)
        self.cg = CoinGeckoAPI()
        
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    def get_exchange_prices(self, ticker: str, search_ticker: bool = True):
        # Get the name from the csv file based on the ticker. 
        if search_ticker:
            name = self.get_coinname_by_ticker(ticker)
        # If we are not searching for a ticker, then a name is passed in the arguement "ticker" instead. 
        elif not search_ticker:
            name = ticker
        url = f"https://api.coingecko.com/api/v3/coins/{name.lower()}"

        response = requests.get(url)
        
        # If request was successful. 
        if response.status_code == 200:
            data = response.json()
            return data["tickers"]
        else:
            raise Exception(f"Unable to retrieve data: {url} {ticker}")

        
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------  Coin Search Operations  -----------------------------------'''
    '''-----------------------------------'''
    def get_coinname_by_ticker(self, ticker: str):
        # Get the row with the matching ticker.

        matching_row = self.coin_ids[self.coin_ids["symbol"] == ticker.lower()]

        if not matching_row.empty:
            name = matching_row.iloc[0]["name"]
            return name
        else:
            return None
    '''-----------------------------------'''
    def get_trending_tickers(self):
        trending_tickers = self.cg.get_search_trending()
        extracted_data = []
        for coin in trending_tickers['coins']:
            coin_data = coin['item']
            extracted_data.append({
                "id": coin_data["id"],
                "coin_name": coin_data["name"],
                "ticker": coin_data["symbol"],
                "marketcap_rank": coin_data["market_cap_rank"]
            })
        return extracted_data
    '''-----------------------------------'''
    def get_coin_list(self):
        return self.cg.get_coins_list()
    '''-----------------------------------'''
    def get_exchange_list(self):
        return self.cg.get_exchanges_list()
    '''-----------------------------------  Data Retrieval Operations  -----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------  CSV Operations  -----------------------------------'''
    '''-----------------------------------'''
    def write_coins_to_csv(self, data):
        pass
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''