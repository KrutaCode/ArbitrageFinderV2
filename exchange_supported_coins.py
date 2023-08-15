ccxt_supported_exchanges = ['ace', 'alpaca', 'ascendex', 'bequant', 'bigone',
                            'binance', 'binancecoinm', 'binanceus', 'binanceusdm',
                            'bingx', 'bit2c', 'bitbank', 'bitbay', 'bitbns',
                            'bitcoincom', 'bitfinex', 'bitfinex2', 'bitflyer', 'bitforex',
                            'bitget', 'bithumb', 'bitmart', 'bitmex', 'bitopro',
                            'bitpanda', 'bitrue', 'bitso', 'bitstamp', 'bitstamp1',
                            'bittrex', 'bitvavo', 'bkex', 'bl3p', 'blockchaincom',
                            'btcalpha', 'btcbox', 'btcmarkets', 'btctradeua', 'btcturk',
                            'bybit', 'cex', 'coinbase', 'coinbaseprime', 'coinbasepro',
                            'coincheck', 'coinex', 'coinfalcon', 'coinmate', 'coinone',
                            'coinsph', 'coinspot', 'cryptocom', 'currencycom', 'delta',
                            'deribit', 'digifinex', 'exmo', 'fmfwio', 'gate', 
                            'gateio', 'gemini', 'hitbtc', 'hitbtc3', 'hollaex',
                            'huobi', 'huobijp', 'huobipro', 'idex', 'independentreserve',
                            'indodax', 'kraken', 'krakenfutures', 'kucoin', 'kucoinfutures',
                            'kuna', 'latoken', 'lbank', 'lbank2', 'luno',
                            'lykke', 'mercado', 'mexc', 'mexc3', 'ndax',
                            'novadax', 'oceanex', 'okcoin', 'okex', 'okex5',
                            'okx', 'paymium', 'phemex', 'poloniex', 'poloniexfutures',\
                            'probit', 'tidex', 'timex', 'tokocrypto', 'upbit',
                            'wavesexchange', 'wazirx', 'whitebit', 'woo', 'yobit',
                            'zaif', 'zonda']


modified_list = ['alpaca', 
                'bitcoincom', 'bitfinex', 'bitfinex2', 'bitflyer', 'bitforex',
                'bitmart', 'bitmex', 'bitopro',
                'coinbase', 'coinbaseprime', 'coinbasepro',
                'gemini', 'kraken', 'krakenfutures', 'kucoin', 'kucoinfutures',
                'mexc', 'okx']



'''
#####################################
Alpaca
#####################################
'''
alpaca_supported_coins = [
    "AAVE", "BAT", "BCH", # 0 - 2
    "BTC", "ETH", "GRT",  # 3 - 5
    "LINK", "LTC", "MKR", # 6 - 8
    "PAXG", "SHIB", "UNI" # 8 - 11
]


'''
#####################################
Coinbase
#####################################
'''
coinbase_supported_coins = ["AAVE", "ACH", "ADA", "AGLD", "ALGO",
                            "AMP", "ANKR", "APE", "ARB", "ATOM",
                            "AUCTION", "AVAX", "AXS", "BCH", "BLUR",
                            "BOND", "BTC", "CBETH", "CHZ", "COMP", 
                            "CRO", "CRPT", "CRV", "DOGE", "DOT", 
                            "EOS", "ERN", "ETC", "ETH", "FET",
                            "FIL", "FLOW", "FORTH", "GRT", "HBAR",
                            "ICP", "IMX", "INJ", "JASMY", "KNC", 
                            "LCX", "LDO", "LINK", "LQTY", "LRC",
                            "LTC", "MANA", "MATIC", "MKR", "NEAR",
                            "OGN", "OP", "PNG", "PRQ", "QNT",
                            "RNDR", "SAND", "SHIB", "SNX", "SOL",
                            "STOR", "STX", "SUKU", "SUSHI", "SWFTC",
                            "SYN", "UNI", "VGX", "XLM", "XRP", "XYO"
                            "YFI", "ZRX"]

'''
#####################################
Kraken
#####################################
'''
kraken_supported_coins = [
   'ZRX','1INCH','AAVE','GHST','ACA','AGLD','AKT','ALCX','ACH','ALGO',
   'TLM','AIR','ADX','FORTH','ANKR','APE','API3','APT','ANT','ARB',
   'ARPA','ASTR','AUDIO','REP','AVAX','AXS','BADGER','BAL',
   'BNT','BAND','BOND','BAT','BSX','BICO','BNC','BTC','BCH','BIT','BTT',
   'BLUR','BLZ','BOBA','FIDA','ADA','CTSI','CELR','CFG','XCN','LINK',
   'CHZ','CHR','CVC','COMP','C98','CVX','ATOM','COTI','CQT','CSM',
   'CRV','DAI','DASH','MANA','DENT','DOGE','DYDX','EWT','ENJ','MLN',
   'EOS','ETHW','ETH','ETC','ENS','EUL','FTM','FET','FIL','FLR',
   'FLOW','FXS','GALA','GAL','GARI','MV','GTC','GMX','GNO','GST',
   'FARM','HFT','HDX','ICX','IDEX','RLC','IMX','INJ','TEER','INTR',
   'ICP','JASMY','JUNO','KAR','KAVA','ROOK','KEEP','KP3R','KILT','KIN',
   'KINT','KSM','KNC','LDO','LCX','LMWR','LSK','LTC','LPT','LRC',
   'MKR','MNGO','MSOL','POND','MASK','MC','MINA','MIR','XMR','GLMR',
   'MOVR','MULTI','EGLD','MXC','ALICE','NANO','NEAR','NODL','NMR','NYM',
   'OCEAN','OMG','ORCA','OXT','OGN','OXY','PARA','PAXG','PEPE','PERP',
   'PHA','PLA','DOT','POLS','MATIC','POWR','PSTAKE','QTUM','QNT','RAD',
   'RARI','RAY','REN','RNDR','REQ','XRP','XRT','RPL','RBC','SBR',
   'SAMO','SCRT','KEY','SRM','SHIB','SDN','SC','SOL','SGB','SPELL',
   'STX','FIS','ATLAS','POLIS','STG','ALPHA','XLM','STEP','GMT','STORJ',
   'SUI','SUPER','RARE','SUSHI','SYN','SNX','TBTC','LUNA',
   'EURT','TVK','XTZ','GRT','SAND','RUNE','T','TOKE',
   'TRX','TRU','TUSD','UNFI','UNI','UMA','WAVES','WOO','WBTC','WAXL','YFI','YGG','ZEC'
]

test_coins = ["BTC", "ETH", "LINK", "MATIC", "ATOM", "CRV"]