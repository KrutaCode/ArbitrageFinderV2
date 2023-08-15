# Operating system related imports 
import os
from dotenv import load_dotenv
load_dotenv()

from web3 import Web3






# Import contracts for DEX
from DEX.dex_contracts import  ContractManager, uniswap_v3, uniswap_v2




'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''
'''-----------------------------------'''






class DexOracle:
    def __init__(self, dex_list: list = []) -> None:
        self.dex_list = dex_list
        infura_key = os.getenv("infura_key")
        uni_address2 = uniswap_v2["uniswapRouterV2"]["address"]
        #uni_address = uniswap_v3["uniswapRouterV3"]["address"]
        self.w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{infura_key}"))
        self.c_man = ContractManager("LINK", "optimism")
        
        abi = self.c_man.set_contract_address("Chainlink")

        print(f"ABI: {abi}")
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''