
import requests

import random

import threading
import queue



proxies = {
    "japan": "https://140.227.69.170:6000",
    "united_states" : "https://52.183.8.192:3128"
}

valid_proxies_text_file = "D:\\Coding\\VisualStudioCode\\Projects\\Python\\ArbitrageFinderV2\\ProxyServer\\valid_proxies.txt"

class ServerManager:
    def __init__(self) -> None:
        # Read the valid proxy addresses from the text file. 
        with open(valid_proxies_text_file, "r") as f:
            self.proxies = f.read().split("\n")

        # Variable to track how many proxies are currently available. 
        self.num_of_proxies = len(self.proxies)
        # Select a proxy from a randomly generated number. The number will stay in bounds with the number of valid proxies. 
        self.cur_proxy_index = random.randint(0, self.num_of_proxies-1)
        # Assign address from the index. 
        self.cur_proxy = self.proxies[self.cur_proxy_index]
    '''-----------------------------------'''
    def create_proxy_server(self, region: str = "united_states"):
        proxy = {
            'https': proxies[region]
        }
        self.cur_proxy = proxy
    '''-----------------------------------'''
    def check_valid_proxies(self):
        q = queue.Queue()
        valid_proxies = []
        
        with open("proxies.txt", "r") as f:
            proxies = f.read().split("\n")
            for p in proxies:
                q.put(p)
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    def check_IP(self):
        if self.cur_proxy == None:
            self.create_proxy_server()
        
        # Get IP details from "ipinfo.io"
        response = requests.get("https://ipinfo.io/json", proxies=self.cur_proxy)

        print(f"""------------------------
Country: {response.json()['country']}
Region: {response.json()['region']}
""")

    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''