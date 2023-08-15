# Operating system related imports 
import os
from dotenv import load_dotenv
load_dotenv()


# Web3 related imports 
from web3 import Web3

# Import oracles
import Oracle.cex_oracle
import Oracle.coin_oracle

# Import dex contracts
import DEX.dex_contracts



class ArbitrageFinder:
    def __init__(self) -> None:
        # Create variables for class objecsts.
        self.cex_oracle = None
        self.coin_oracle = Oracle.coin_oracle.CoinOracle()
        self.contract_manager = DEX.dex_contracts.ContractManager()

        self.stable_coins = ["USD", "USDC", "USDT"]
        self.excluded_exchanges = ["XT.COM"]


    
    '''-----------------------------------'''
    def create_cex_oracle(self, cex_list: list, ticker_list: list):
        self.cex_list = cex_list
        self.ticker_list = ticker_list
        self.cex_oracle = Oracle.cex_oracle.CexOracle(cex_list=cex_list, ticker_list=ticker_list)
    '''-----------------------------------'''
    
    
    '''-----------------------------------'''
    def find_arbitrage_cex(self):
        '''
        
        Description: Retrieves data from the centralized exchanges and compares their prices. 
        Each exchange will be compared against eachother and measure if there is any notable %  difference. 
        
        '''
        exchange_data = self.cex_oracle.get_prices_thread()

        compared_data = {}
        for symbol, value in exchange_data.items():   
           for i in range(len(value)):
                exchange1 = value[i]["exchange"]
                data1 = value[i]["data"]
                close_price1 = data1["close"]
                for j in range(len(value)):
                    # Pass matching indexes. There is no point in comparing prices from the same exchange. 
                    if j == i:
                        pass
                    else:
                        exchange2 = value[j]["exchange"]
                        data2 = value[j]["data"]
                        close_price2 = data2["close"]
                        perc_diff = ((close_price1/close_price2) - 1) * 100

                        if symbol not in compared_data:
                            compared_data[symbol] = []


                        compared_data[symbol].append({
                            "exchange1" : exchange1,
                            "exchange2": exchange2,
                            "ticker": symbol,
                            "price1": close_price1,
                            "price2": close_price2,
                            "perc_diff": perc_diff
                        })

        # Sort the data sort the data where larger "perc_diff" instances come first.
        for ticker in compared_data:
            compared_data[ticker] = sorted(compared_data[ticker], key=lambda x: x['perc_diff'], reverse=True)

        # Initialize to negative infinity. This is so the logic can handle negative values. 
        max_perc_diff = -float("inf")

        for ticker, ticker_data in compared_data.items():
            max_ticker_diff = max(ticker_data, key=lambda x: x["perc_diff"])["perc_diff"]
            if max_ticker_diff > max_perc_diff:
                max_perc_diff = max_ticker_diff
                best_ticker = ticker
        print(f"The ticker with the highest perc_diff is {best_ticker} with a value of {max_perc_diff}")
        print(f"Compared: {compared_data}")
    '''-----------------------------------'''
    '''-----------------------------------'''
    def find_arbitrage_mixed(self, coin_list: list, search_ticker: bool = False):
        '''
        '''

        exchange_data = []

        for c in coin_list:
            # Get the coin id.
            coin_id = c["id"]

            # Get the prices of the coin on each exchange.
            coin_price_data = self.coin_oracle.get_exchange_prices(coin_id, search_ticker=False)
            # Compare each exchange against eachother.
            exchange_routes = self.compare_exchange_prices(coin_price_data)
            exchange_data.append(exchange_routes)

        return exchange_data
    '''-----------------------------------'''
    def compare_exchange_prices(self, data: list):
        index = 0

        total_routes = []
        for i in range(len(data)):
            # Get the exchange data to use as a reference point. 
            ref_exchange = data[i]
            ref_base, ref_target, ref_exchange_name = ref_exchange["base"], ref_exchange["target"], ref_exchange["market"]["name"]

            # Check if the target coin is a stable coin. If not get from the "converted_last" field.
            if ref_target not in self.stable_coins:
                ref_price = ref_exchange["converted_last"]["usd"]
            else:
                ref_price = ref_exchange["last"]

            # Check if the reference price is in scientific notation.
            if self.is_scientific_notation(ref_price):
                ref_price = format(ref_price, ".20f")
            
            if self.is_address(ref_base):
                ref_exchange_type = "DEX"
            else:
                ref_exchange_type = "CEX"

            # Iterate through the other exchanges to compare the reference exchange to. 
            exchange_routes = []
            for j in range(len(data)):
                target_exchange = data[j]
                target_base, target_target, target_exchange_name = target_exchange["base"], target_exchange["target"], target_exchange["market"]["name"]

                # Check if either of the exchanges are in the list of "excluded_exchanges"
                if ref_exchange_name not in self.excluded_exchanges and target_exchange_name not in self.excluded_exchanges: 
                    # If the exchanges are not the same. 
                    if target_exchange_name != ref_exchange_name:
                        if target_target not in self.stable_coins:
                            target_price = target_exchange["converted_last"]["usd"]
                        else:
                            target_price = target_exchange["last"]

                        # Check if the price is in scientific notation.
                        if self.is_scientific_notation(target_price):
                            target_price = format(target_price, ".20f")


                        # Calculate the percentage difference between the target price and the reference price. 
                        perc_diff = ((target_price/ref_price) - 1) * 100

                        if self.is_address(target_base):
                            target_exchange_type = "DEX"
                        else:
                            target_exchange_type = "CEX"


                        # Create a dictionary to hold the pair data. 
                        pair_data = {
                        "source_exchange": ref_exchange_name,
                        "exchange_path": f"{ref_exchange_name} -> {target_exchange_name}",
                        "exchange_types": f"{ref_exchange_type}:{target_exchange_type}",
                        "reference_pair": f"{ref_base}/{ref_target}",
                        "target_pair": f"{target_base}/{target_target}",
                        "reference_price": ref_price,
                        "target_price": target_price,
                        "perc_diff": perc_diff 
                        }

                        exchange_routes.append(pair_data)

            # Check if the list is not empty. This is to avoid adding empty fields to the list. 
            # Empty fields occur when the exchange being searched is in the "excluded_list".  
            if exchange_routes != []:
                total_routes.append(exchange_routes)

        # Sort the inner list. 
        sorted_routes = self.sort_routes(total_routes)
        # Sort the outer list. 
        sorted_routes.sort(key=lambda x: x[0]["perc_diff"], reverse=True)
        print(f"{sorted_routes}")
        return sorted_routes
    '''-----------------------------------'''
    def sort_routes(self, route):
        # Sort the inner list first.
        sorted_routes = [sorted(r, key=lambda x: x["perc_diff"], reverse=True) for r in route]
        return sorted_routes
    '''-----------------------------------'''
    def is_address(self, input_str: str) -> bool:

        if len(input_str) >= 8:
            if input_str.startswith("0x") or input_str.startswith("0X"):
                return True
        return False
    '''-----------------------------------'''
    def convert_address_to_ticker(self, address: str):
        infura_key = os.getenv("infura_key")
        w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{infura_key}"))

        # Convert the contract address to checksum format.
        contract_address = w3.to_checksum_address(address)

        # Get the abi.
        abi = self.contract_manager.get_contract_abi(address)

        # Create a contract instance.
        token_contract = w3.eth.contract(address=contract_address, abi=abi)

        # Retrieve token symbol and name
        token_symbol = token_contract.functions.symbol()
        return token_symbol
    '''-----------------------------------'''
    def is_scientific_notation(self, num):
        num_str = str(num)
        return 'e' in num_str or 'E' in num_str
    '''-----------------------------------'''
    def display_arbitrage(self, data, include_rows: int = 3):

        for item in data:
            ticker = item[0][0]["reference_pair"].split("/")[0]
            for i in range(include_rows):
                exchange_path1 = item[0][i]["exchange_path"]
                exchange_type = item[0][i]["exchange_types"]
                base_price = item[0][i]["reference_price"]
                target_price = item[0][i]["target_price"]
                perc_diff = "{:.2f}".format(item[0][i]["perc_diff"])



                print(f"""
----------------------------------------
{ticker}
Path: {exchange_path1}
Type: {exchange_type}
Base Price: {base_price}
Target Price: {target_price}
% Difference: {perc_diff} %

                """)



            

    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''