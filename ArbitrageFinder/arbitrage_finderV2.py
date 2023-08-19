
import json

# Time and date related imports
import time
import datetime as dt

# Import oracles
import Oracle.coin_oracle



arbitrage_text_file = "D:\\Coding\\VisualStudioCode\\Projects\\Python\\ArbitrageFinderV2\\arbitrage_routes.txt"


class ArbitrageFinderV2:
    def __init__(self) -> None:
        self.coin_oracle = Oracle.coin_oracle.CoinOracle()
        self.stable_coins = ["USD", "USDC", "USDT"]
        self.arbitrage_routes = {}
        self.excluded_exchanges =  ["Binance", "Biswap","BitBNS", "Bitfinex", "Bitkub", "Bithumb" "Bybit",
                                    "CoinDCX", "CoinTiger", "Energiswap", "HitBTC", "Icrypex", "Indodax",
                                    "SafeTrade", "THENA FUSION" "Upbit", "WarzirX" "XT.COM", "ZebPay"]
        
        self.excluded_coins = ["INJ", "TWT"]
    '''-----------------------------------'''
    def find_arbitrage_routes(self, coin_list: list, arbitrage_minimum: float = 0.0):
        '''
        Takes a list of coins as the parameter. It will loop through each coin and find the most efficient paths
        between exchanges to maximize arbitrage profits. 
        
        coin_list: list of coin names. 
        arbitrage_minimum: The minimum arbitrage spread a route must meet to be included in the data. 
        '''

        # Loop through list of coins. 
        for coin in coin_list:
            # Get the coin id.
            coin_id = coin["id"]
            # Get the prices from the exchanges that it trades on. 
            exchange_price_data = self.coin_oracle.get_exchange_prices(coin_id)
            # Compare the prices on each exchange. 
            data = self.compare_exchange_prices(exchange_price_data, arbitrage_minimum)
            self.arbitrage_routes[coin_id] = data
 


    '''-----------------------------------'''
    def compare_exchange_prices(self, exchange_data: list, arbitrage_minimum: float = 0.0):
        '''
        Takes the price of a coin on one exchange and compares it with the price of the same coin on another exchange. 
        It will then calculate the difference between the coins in terms of a percentage. 
        '''
        
        datetime_string = str(dt.datetime.now().isoformat())
        date_time_parts = datetime_string.split("T")
        date_without_fraction = date_time_parts[0] + " " + date_time_parts[1].split(".")[0]
        time_retrieved = date_without_fraction
        path_performance = {}
        exchanges = {}
        for i in range(len(exchange_data)):
            # Tracks performance of the path. 
            positive_arb, negative_arb = 0, 0
            ref_exchange = exchange_data[i]
            # Get the base and target coin of the pair. Ex: base=BTC, target=USDC -> BTC/USDC
            ref_base, ref_target = ref_exchange["base"], ref_exchange["target"]
            # Get the name of the exchange and price from the exhcange.
            ref_exchange_name = ref_exchange["market"]["name"]

            # Check that the reference exchange is not in the "excluded_exchanges list". 
            if ref_exchange_name not in self.excluded_exchanges and ref_exchange_name != "THENA FUSION":


                ref_price = ref_exchange["last"]
                ref_stale_state = ref_exchange["is_anomaly"]
                ref_anomaly_state = ref_exchange["is_stale"]
                ref_trust_score = ref_exchange["trust_score"]

                # Check if the target coin is a stable coin. If not get from the "converted_last" field.
                if ref_target not in self.stable_coins:
                    ref_price = ref_exchange["converted_last"]["usd"]
                else:
                    ref_price = ref_exchange["last"]


                # Get the exchange type. Pass the base pair to the function. 
                # Will return CEX if a ticker is passed. Will return DEX if a contract address is passed.
                ref_exchange_type = self.get_exchange_type(ref_base)
                # Create the pair for the reference exchange.
                ref_pair = f"{ref_base}/{ref_target}"

                

                for j in range(len(exchange_data)):
                    comp_exchange = exchange_data[j]
                    if j == i:
                        pass
                    else:
                        comp_exchange = exchange_data[j]
                        # Get the base and target coin of the coin we are comparing. 
                        comp_base, comp_target = comp_exchange["base"], comp_exchange["target"]
                        # Get the name and price from the target exchange.
                        comp_exchange_name = comp_exchange["market"]["name"]


                        # Check if either of the exchanges are in the list of "excluded_exchanges"
                        if comp_exchange_name not in self.excluded_exchanges: 
                            comp_price = comp_exchange["last"]
                            # Check if the target coin is a stable coin. If not get from the "converted_last" field.
                            if comp_target not in self.stable_coins:
                                comp_price = comp_exchange["converted_last"]["usd"]
                            else:
                                comp_price = comp_exchange["last"]

                            comp_pair = f"{comp_base}/{comp_target}"
                            # Get the exchange type.
                            comp_exchange_type = self.get_exchange_type(comp_base)
                            # Create the pair for the target exchange.
                            comp_pair = f"{comp_base}/{comp_target}"
                            comp_stale_state = comp_exchange["is_stale"]
                            comp_anomaly_state = comp_exchange["is_anomaly"]
                            comp_trust_score = comp_exchange["trust_score"]

                            # Calculate the percentage difference between the comparison exchange and the reference exchange.
                            perc_diff = ((comp_price - ref_price)/abs(ref_price)) * 100

                            # If perc_diff is greater than "arbitrage_minimum" append the data.
                            if perc_diff >= arbitrage_minimum:
                                data = {
                                    "time_retrieved": time_retrieved,
                                    "route_path": f"{ref_exchange_name} -> {comp_exchange_name}   ({ref_exchange_type}):({comp_exchange_type})",
                                    "perc_diff": perc_diff,
                                    "reference_exchange": {
                                        "exchange_name": ref_exchange_name,
                                        "pair": ref_pair,
                                        "base": ref_base,
                                        "target": ref_target,
                                        "price": ref_price,
                                        "stale": ref_stale_state,
                                        "anomaly": ref_anomaly_state,
                                        "trust_score": ref_trust_score
                                    },
                                    "comparison_exchange": {
                                        "exchange_name": comp_exchange_name,
                                        "pair": comp_pair,
                                        "base": comp_base,
                                        "target": comp_target,
                                        "price": comp_price,
                                        "stale": comp_stale_state,
                                        "anomaly": comp_anomaly_state,
                                        "trust_score": comp_trust_score
                                    }

                                }
                            # Check if a key for the current exchange does not exist yet. 
                            if ref_exchange_name not in exchanges:
                                exchanges[ref_exchange_name] = []

                            # Only add the value if it is positive.
                            if perc_diff > 0:
                                positive_arb += 1
                                # At append data to the list at the key associated with the exchange. 
                                exchanges[ref_exchange_name].append(data)
                            else:
                                negative_arb += 1
                    
            try:
                performance = (positive_arb/(positive_arb + negative_arb)) * 100
                # Check if a key for the exchange does not exist. If not set it to an empty dictionary.
                if ref_exchange_name not in path_performance:
                    # Add data to the exchange key.
                    path_performance[ref_exchange_name] = {
                    "positive_arb": positive_arb,
                    "negative_arb": negative_arb, 
                    "performance": performance
                    }
                else:
                    path_performance[ref_exchange_name]["positive_arb"] += positive_arb
                    path_performance[ref_exchange_name]["negative_arb"] += negative_arb
                    performance = (positive_arb/(positive_arb + negative_arb)) * 100
                    path_performance[ref_exchange_name]["performance"] = performance
            except ZeroDivisionError:
                pass

        # Add the perfomance value to the associated exchange key. 
        final_data = {}
        for key, value in exchanges.items():
            # If key does not exist in dict, assign empty values to them. 
            if key not in final_data:
                final_data[key] = {"path" : []}
                final_data[key] = {"performance": 0.0}
                final_data[key] = {"positive_routes": 0}
                final_data[key] = {"negative_routes": 0}
                final_data[key] = {"total_routes": 0}
            
            # Add values to relevant paths. 
            final_data[key]["path"] = sorted(value, key=lambda x: x["perc_diff"], reverse=True)
            final_data[key]["performance"] = "{:.2f}".format(path_performance[key]["performance"])
            final_data[key]["positive_routes"] = path_performance[key]["positive_arb"]
            final_data[key]["negtive_routes"] = path_performance[key]["negative_arb"]
            final_data[key]["total_routes"] = path_performance[key]["positive_arb"] + path_performance[key]["negative_arb"]
            
        return final_data

    '''-----------------------------------'''
    def get_top_routes(self, coin_list: list = [], limit: int = 10):
        # Check if there are arbitrage routes. Otherwise, set new routes. 
        if self.arbitrage_routes == {}:
            self.find_arbitrage_routes(coin_list)
        

        # List to hold all routes. 
        all_routes = []

        # Iterate through each coin. 
        for coin, value in self.arbitrage_routes.items():

            for k, v in value.items():
                for i in v["path"]:
                    
                    ref_base, ref_target = i["reference_exchange"]["base"], i["reference_exchange"]["target"]
                    comp_base, comp_target = i["comparison_exchange"]["base"], i["comparison_exchange"]["target"]
                    if ref_base not in self.excluded_coins and ref_target not in self.excluded_coins:
                        if comp_base not in self.excluded_coins and comp_target not in self.excluded_coins:
                            all_routes.append(i)

        
        # Sort the routes 
        all_routes = sorted(all_routes, key=lambda x: x["perc_diff"], reverse=True)
        # Get the length to get the total number of routes. 
        self.num_of_routes = len(all_routes)
        # Check if the number of routes is less than the amount of routes requested. 
        if self.num_of_routes < limit:
            # If it is less than, default the value to the length of "all_routes". 
            # This way if the user requests more paths than exist, the whole list will be returned. 
            limit = self.num_of_routes


        top_routes = all_routes[:limit]

        return top_routes

    '''-----------------------------------'''
    def write_top_routes(self, top_routes = None, limit:int = 20):
        if top_routes == None:
            print(f"Limit: {limit}")
            top_routes = self.get_top_routes(limit=limit)
        
        with open(arbitrage_text_file, "w") as file:
            json.dump(top_routes, file, indent=4)
    '''-----------------------------------'''
    def get_exchange_type(self, input_str):
        '''
        If a ticker for a coin is passed, it most likely came from a CEX.
        If an address is passed as the input, it is most likely a DEX.
        This is because the coin gecko api will use the raw token contract address,
        instead of displaying the ticker when using DEX pairs. 
        '''
        # Boolean to determine if the input is an address. 
        is_address = self.is_address(input_str=input_str)

        if is_address:
            return "DEX"
        else:
            return "CEX"

    '''-----------------------------------'''
    def is_address(self, input_str: str) -> bool:
        # Check if the string is longer than at least 8 characters.
        if len(input_str) >= 8:
            # Check if string starts with common address characters. 
            if input_str.startswith("0x") or input_str.startswith("0X"):
                return True
        return False
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''