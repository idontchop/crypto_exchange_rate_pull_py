import cryptsymarketpull
import coinse_pull
import poloniex_pull
import bter_pull
import coinex_pull
import mintpal_pull
import vircurex_pull
import btce_pull
import time

base_markets_used = ['BTC','LTC'] # used by build_exchange_coin_list to sync with call to api

base_markets_list = { 'BTC':['42','ANC','ASC','AUR','BET','BFC','BOC','BTE','BQC','CAP','CAT','CGB','CMC','CTM','DEM','DGC',
                    'DOGE','EAC','EXC','FLAP','FFC','FRE','FST','FTC','GLD','GDC','GRW','HBN','IFC','IXC','LKY','LOT',
                    'LTC','MAX','MEC','MINT','MNC','MOON','MZC','NEC','NET','NOBL','NVC','NXT','OSC','PHS','PPC','PXC','PYC','REDD','RPC','SMC',
                    'SRC','SXC','TAG','TEA','TEK','TGC','TRC','UNO','USDE','VTC','WDC','XJO','XPM','ZEIT',
                    'ZET'],
                      'LTC':[]
                      }

""" for each entry in markets_list, we can check if it exists in
exchange_list and then the function to call is available
so we can write one piece of cose for btc and ltc instead of seperate
codes for each exchange"""

exchange_list = {'cryptsy':
                 {  'name': 'Cryptsy',
                    'url': 'http://www.cryptsy.com',
                    'BTC': ['DOGE'],
                    'LTC': ['DOGE'],
                    'call': cryptsymarketpull.cryptsy ,
                    'callcoins': cryptsymarketpull.cryptsy_coins },
                 'poloniex':
                 { 'BTC': ['DOGE'],
                   'LTC': [],
                   'call': poloniex_pull.poloniex ,
                   'callcoins': poloniex_pull.poloniex_coins },
                 'coinse':
                 { 'BTC': ['AMC','ANC','AUR','BQC','DOGE','GRD','FTC','GLB','LTC','MAX','NET',
                           'WDC','ZET','TAG'],
                   'LTC': [],
                   'call': coinse_pull.coinse },
                 'bter':
                 { 'BTC': ['DOGE','BQC','CMC','DGC','EXC','FTC','MAX','MEC','MINT','NEC',
                           'NXT','TAG','VTC','WDC','XPM','ZET'],
                   'LTC': [],
                   'call': bter_pull.bter,
                   'callcoins': bter_pull.bter_coins },
                 'coinex':
                 { 'BTC': ['ANC','ASC','BET','BFC','BOC','CAP','CAT','CGB','CMC','CTM','DGC','DOGE',
                           'EXC','FST','FTC','GLD','HBN','IFC','LKY','LOT','LTC','MEC','MNC','NEC','NOBL',
                           'NVC','OSC','PHS','PPC','PXC','PYC','SMC','SRC','SXC','TAG','VTC','WDC','XPM','ZEIT',
                           'ZET'],
                   'LTC': ['DOGE'],
                   'call': coinex_pull.coinex },
                 'mintpal':
                 { 'BTC': ['DOGE','AUR','CTM','DGB','DOGE','MZC','USDE','LTC',
                           'MINT'],
                   'LTC': [],
                   'call': mintpal_pull.mintpal,
                   'callcoins': mintpal_pull.mintpal_coins},
                 'vircurex':
                 { 'BTC': ['ANC','DOGE','LTC','DGC','FTC','NXT','WDC','XPM'],
                   'LTC': [],
                   'call': vircurex_pull.vircurex },
                 'btce':
                 { 'BTC': ['LTC','NMC','NVC','TRC','PPC','FTC','XPM'],
                   'LTC': [],
                   'call': btce_pull.btce }
                 }
                
             
c = {}

def build_exchange_coin_list():
    """this function will be called once at the start of the program
    It will cycle through the exchanges_list dictionary.  If the exchange
    has an API to call for a currency list, it will replace the currency lists
    currently defined """
    global exchange_list
    global base_markets_list
    for exchange in exchange_list:
        if 'callcoins' in exchange_list[exchange].keys():
            exchange_coin_list = exchange_list[exchange]['callcoins']()
            if exchange_coin_list['found'] == True:
                for base in base_markets_used:
                    exchange_list[exchange][base] = list(set(exchange_list[exchange][base] + exchange_coin_list[base]))  #update exchange list
                    base_markets_list[base] = list(set(exchange_list[exchange][base] + base_markets_list[base]))                           #update base list

def find_coin_markets(coin='NET',base='BTC'):
    """ this function will be used by user input to find which markets a certain
    pair is available at """

    for exchange in exchange_list:
        if coin in exchange_list[exchange][base]:
            print (exchange + "\n")
                    
def run_btc_finder():
    """ use btc_markets_list() to loop through the coins in btc trade
    """
    base = 'BTC'
    for coin in base_markets_list[base]:
        bestbid = 0
        bidexchange = ""
        bestask = 1000000000
        askexchange = ""
        for exchange in exchange_list:
            if coin in exchange_list[exchange][base]:
                c = exchange_list[exchange]['call'](coin)
                if c['found'] == False:
                    print ("didn't find " + coin + " in " + exchange)
                    continue
                if c['bestbid'] > bestbid:
                    bestbid = c['bestbid']
                    bidexchange = exchange
                if c['bestask'] < bestask:
                    bestask = c['bestask']
                    askexchange = exchange
        #print (coin + " {:.8f} ".format(bestbid) + bidexchange + " {:.8f} ".format(bestask) + askexchange)
        if (bestask < bestbid): # print dollar signs, if an ask is less than a bid, instant trade profit
            diff = (bestask - bestbid) * -100000000 # change to satoshi
            percentage = 100 - (100 * (bestask/bestbid))
            print ("Profitable trade found {:.0f}".format(diff) + " satoshi, {:.2f}%".format(percentage) + " in " + coin + ":\n")
            print ("Bid: {:.8f} ".format(bestbid) + bidexchange)
            print ("Ask: {:.8f} ".format(bestask) + askexchange)
                   



#rough test of each market
def rough_print(coins_array):
    for coin in coins_array:
        #cryptsy
        coin_dict = cryptsymarketpull.cryptsy(coin)
        if coin_dict['found'] == False:
            print("Didn't find " + coin + " on cryptsy")
            continue
        print(coin + "/BTC on cryptsy:\nBID: {:.8f}".format(coin_dict['bestbid']) + "\nASK: {:.8f}".format(coin_dict['bestask']))
        #coins-e
        coin_dict = coinse_pull.coinse(coin)
        if coin_dict['found'] == False:
            print("Didn't find " + coin + "on coins-e")
            continue
        print(coin + "/BTC on coins-e:\nBID: {:.8f}".format(coin_dict['bestbid']) + "\nASK: {:.8f}".format(coin_dict['bestask']))
        #poloniex
        coin_dict = poloniex_pull.poloniex(coin)
        if coin_dict['found'] == False:
            print("Didn't find " + coin + "on poloniex")
            continue
        print(coin + "/BTC on poloniex:\nBID: {:.8f}".format(coin_dict['bestbid']) + "\nASK: {:.8f}".format(coin_dict['bestask']))
    
build_exchange_coin_list()
print(exchange_list['cryptsy']['BTC'])
#print(str(len(exchange_list['cryptsy']['BTC'])))
#print(base_markets_list['BTC'])
#print(str(len(base_markets_list['BTC'])))

#find_coin_markets()
#run_btc_finder()

"""
coins_array_draft = ['ANC', 'LTC', 'DOGE']

full_str = input("Enter coins or press enter for default: ")
coins_array = full_str.split()
if len(coins_array) == 0: coins_array = coins_array_draft
rough_print(coins_array)
"""
