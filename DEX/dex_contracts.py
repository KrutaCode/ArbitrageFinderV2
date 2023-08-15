import requests




uniswap_v2 = {"uniswapRouterV2": {"address":"0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"}}


uniswap_v3 = {"uniswapRouterV3": {"address": "0x1F98431c8aD98523631AE4a59f267346ea31F984"}}

# ERC-20 ABI (Application Binary Interface)
erc20_abi = [
    {"inputs": [], "stateMutability": "view", "type": "function", "name": "symbol", "outputs": [{"name": "", "type": "string"}]},
    {"inputs": [], "stateMutability": "view", "type": "function", "name": "name", "outputs": [{"name": "", "type": "string"}]}
]





'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''



class ContractManager:
    def __init__(self) -> None:

        # Variables to hold contract data. 
        self.address = ""
        self.abi = None

    '''-----------------------------------'''
    def set_contract_abi(self, address: str):
        base_url = "https://api.etherscan.io/api?module=contract&action=getabi&address={}".format(address)

        # Make a request to the Etherscan api.
        response = requests.get(base_url)

        # Check for errors.
        if response.status_code != 200:
            raise Exception(f"Error retrieving ABI from etherscan: {base_url}")

        # Get the abi response.
        self.abi = response.json()["result"]
        
    '''-----------------------------------'''
    def get_contract_abi(self, address: str = ""):
        if self.address == "":
            self.set_contract_abi(address)
        return self.abi
    '''-----------------------------------'''
    def set_contract_address(self, name:str):
        url = f"https://api.coingecko.com/api/v3/coins/{name.lower()}"
        print(f"URL: {url}")
        response = requests.get(url)
        data = response.json()

        print(f"Data: {data['tickers']}")

        if 'platform' in data and self.network in data["platforms"]:
            print(f"Data: {data['platforms'][self.network]}")
        print(f"Data: {data['platforms'].keys()}")
        #print(f"Data: {data}")
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
