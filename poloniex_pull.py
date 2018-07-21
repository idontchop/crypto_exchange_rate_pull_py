import urllib.request
import json

#poloniex get list

def poloniex_coins():
    poloniex_ticker_api = "https://poloniex.com/public?command=returnTicker"
    yawn = {'User-Agent' : 'minerjeff'}
    coin_dict = {'found':True}
    request = urllib.request.Request(poloniex_ticker_api, None, yawn)
    try: full = str(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
                print(e)
                print(poloniex_ticker_api)
                coin_dict = {'found':False}
                return coin_dict
    try: json_data = json.loads(full[2:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict

    for exchange in json_data:
        label = exchange.split('_')
        base = label[0].upper()
        coin = label[1].upper()
        if base in coin_dict.keys():
            coin_dict[base].append(coin)
        else:
            coin_dict[base] = [coin]

    return coin_dict

# poloniex has a depth type API  (along with btce and bter)

def poloniex(coin,base="btc"):
    tradepair = base.upper() + '_' + coin.upper() ## poloniex likes the base first in its pairs
    poloniex_order_api = 'https://poloniex.com/public?command=returnOrderBook&currencyPair=' + str(tradepair)
    """yawn = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'User-Agent' : 'minerjeff'}"""
    yawn = {'User-Agent' : 'minerjeff'}
    coin_dict = {'found':True}
    request = urllib.request.Request(poloniex_order_api, None, yawn)
    try: full = str(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
                print(e)
                print(tradepair)
                coin_dict = {'found':False}
                return coin_dict
    #to get JSON, need to remove b' from beginning and ' from end
    try: json_data = json.loads(full[2:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict
    if 'bids' in json_data:
        coin_dict['found'] = True
    else: # hmm, something wrong
        coin_dict['found']=False
        return coin_dict

    print (json_data);
    bestbid = 0 
    for rate in json_data['bids']:
        if rate[0] > bestbid:bestbid=rate[0]

    bestask = 1000000000
    for rate in json_data['asks']:
        if rate[0] < bestask:bestask=rate[0]

    if bestbid == 0:
        #bestbid still is 0 meaning it found bids but no numbers?  weird
        coin_dict['found'] = False
        return coin_dict
    else:
        coin_dict['bestbid'] = bestbid
        coin_dict['bestask'] = bestask
        return coin_dict
    
#print(poloniex("flap"))

#print(poloniex_coins())
