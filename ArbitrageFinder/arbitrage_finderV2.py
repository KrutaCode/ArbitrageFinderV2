
import json


# Import oracles
import Oracle.coin_oracle






class ArbitrageFinderV2:
    def __init__(self) -> None:
        self.coin_oracle = Oracle.coin_oracle.CoinOracle()
        self.stable_coins = ["USD", "USDC", "USDT"]

        self.excluded_exchanges = ["XT.COM"]
    '''-----------------------------------'''
    def find_arbitrage_routes(self, coin_list: list, arbitrage_minimum: float = 0.0):

        exchange_data = []
        for coin in coin_list:
            # Get the coin id.
            coin_id = coin["id"]
            # Get the prices from the exchanges that it trades on. 
            exchange_price_data = self.coin_oracle.get_exchange_prices(coin_id)
            # Compare the prices on each exchange. 
            self.compare_exchange_prices(exchange_price_data, arbitrage_minimum)

    '''-----------------------------------'''
    def compare_exchange_prices(self, exchange_data: list, arbitrage_minimum: float = 0.0):
        '''
        Takes the price of a coin on one exchange and compares it with the price of the same coin on another exchange. 
        It will then calculate the difference between the coins in terms of a percentage. 
        '''
        
        path_performance = {}
        #print(f"Exchange Data: {exchange_data}")
        exchanges = {}
        for i in range(len(exchange_data)):
            # Tracks performance of the path. 
            positive_arb, negative_arb = 0, 0
            ref_exchange = exchange_data[i]
            # Get the base and target coin of the pair. Ex: base=BTC, target=USDC -> BTC/USDC
            ref_base, ref_target = ref_exchange["base"], ref_exchange["target"]
            # Get the name of the exchange and price from the exhcange.
            ref_exchange_name = ref_exchange["market"]["name"]
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
                    if ref_exchange_name not in self.excluded_exchanges and comp_exchange_name not in self.excluded_exchanges: 
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
                                "route_path": f"{ref_exchange_name} -> {comp_exchange_name}   ({ref_exchange_type}):({comp_exchange_type})",
                                "perc_diff": perc_diff,
                                "reference_exchange": {
                                    "exchange_name": ref_exchange_name,
                                    "pair": ref_pair,
                                    "price": ref_price,
                                    "stale": ref_stale_state,
                                    "anomaly": ref_anomaly_state,
                                    "trust_score": ref_trust_score
                                },
                                "comparison_exchange": {
                                    "exchange_name": comp_exchange_name,
                                    "pair": comp_pair,
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
            print(f"Value: {value}")
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
            

        print(json.dumps(final_data, indent=4))
            

    '''-----------------------------------'''
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