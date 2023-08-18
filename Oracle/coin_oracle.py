# Operating system related imports 
import os
from dotenv import load_dotenv
load_dotenv()

# Web3 related imports
from web3 import Web3
from web3.exceptions import NoABIFound


# Date * Time realted imports
import time 
import datetime as dt

# Requests related imports 
import requests
from requests import Session

# Pandas related imports
import pandas as pd


# Imports for website data sources
from pycoingecko import CoinGeckoAPI
import coinmarketcap


coin_id_path = "D:\\Coding\\VisualStudioCode\\Projects\\Python\\ArbitrageFinderV2\\CoinStorage\\cg_coin_id.csv"
coin_supply_path = "D:\\Coding\\VisualStudioCode\\Projects\\Python\\ArbitrageFinderV2\\CoinStorage\\cg_coin_supply.csv"


network_rpcs = {
    "ethereum": "https://mainnet.infura.io/v3/{}",
    "optimism": "https://optimism.rpc.chain.link/"
}



class CoinOracle:
    def __init__(self) -> None:

        self.coin_ids = pd.read_csv(coin_id_path)
        self.cg = CoinGeckoAPI()

        cmc_key = os.getenv("coinmarketcap_key")

        headers = {
                "Accepts": "application/json",
                "X-CMC_PRO_API_KEY": cmc_key 
            }
        
        self.cmc_session = Session()
        self.cmc_session.headers.update(headers)
        
        
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    def get_exchange_prices(self, ticker: str, search_ticker: bool = False):
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
    def get_coinname_by_address(self, address, network: str = "ethereum"):
        
        rpc_url = None

        # if the network is ethereum get the infura api key. 
        if network == "ethereum":
            # Get infura key from environment variables. 
            infura_key = os.getenv("infura_key")
            rpc_url = network_rpcs["ethereum"].format(infura_key)
        else:
            rpc_url = network_rpcs[network]
        # Create web3 instance
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        # Convert address to checksum format. 
        checksum_address = web3.to_checksum_address(address)
        # Get the abi of the contract. 
        abi = self.get_contract_abi(address=checksum_address)

        # Create contract variable based on address and abi. 
        try:
            token_contract = web3.eth.contract(address=checksum_address, abi=abi)
        # Typically occurs if there is a problem with the abi. 
        except TypeError as e:
            pass
        name = token_contract.functions.name().call()
        print(f"Name: {name}")
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------  Data Retrieval Operations  -----------------------------------'''
    
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
    '''-----------------------------------'''
    def get_contract_abi(self, address: str):
        base_url = "https://api.etherscan.io/api?module=contract&action=getabi&address={}".format(address)

        # Make a request to the Etherscan api.
        response = requests.get(base_url)

        # Check for errors.
        if response.status_code != 200:
            raise Exception(f"Error retrieving ABI from etherscan: {base_url}")

        # Get the abi response.
        return response.json()["result"]
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------  CSV Operations  -----------------------------------'''
    '''-----------------------------------'''
    def write_coins_to_csv(self, data):
        pass
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''