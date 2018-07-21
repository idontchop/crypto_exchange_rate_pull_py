import urllib.request
import json

cryptsy_market_api = 'http://pubapi.cryptsy.com/api.php?method=marketdatav2'
cryptsy_market_data = {}

def call_cryptsy(coincall = "None"):
    """since we don't really know which function we will be calling cryptsy from
    returns False on fail
    """
    global cryptsy_market_data
    yawn = {'User-Agent' : 'minerjeff'}
    request = urllib.request.Request(cryptsy_market_api,None, yawn)
    try: full = str(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
            print(e)
            print(coincall)
            return False
    try: cryptsy_market_data = json.loads(full[2:full.__len__()-1])
    except ValueError:
        print("couldn't lose cryptsy market")
        print(coincall)
        return False
    return True

def cryptsy_coins():
    """ returns a dictionary for all the coins traded on cryptsy in format:
    {'btc': [...],
    'ltc': [...],
    'doge': [...]}
    """
    if 'return' in cryptsy_market_data.keys(): # do nothing
        coin_dict = {'found': True }
    else:
        if(call_cryptsy("None") == False):
            coin_dict = {'found':False}
            return coin_dict
        else: coin_dict = {'found':True}
        
    #start finding the markets
    for market in cryptsy_market_data['return']['markets']:
        label = market.split('\/')
        label[0] = label[0].upper() # double check upper
        label[1] = label[1].upper()
        if label[1] in coin_dict.keys():
            coin_dict[label[1]].append(label[0])
        else:
            coin_dict[label[1]] = [label[0]]
            

    return coin_dict

    

def cryptsy(coin,base="btc"):
    #first see if we already have the data so we don't have to get
    coincall = coin.upper() + '\/' + base.upper()
    coin_dict = {'found': True}
    global cryptsy_market_data
    if 'return' in cryptsy_market_data.keys(): #do nothing
        coin_dict['found'] = True
    else:
        #else we need to query cryptsy
        if(call_cryptsy(coincall) == False):
            coin_dict = {'found':False}
            return coin_dict

#since we can count on the best buy and ask being the first in the set, a simple assign will work for now
    if coincall in cryptsy_market_data['return']['markets']:
        coin_dict['bestbid'] = float(cryptsy_market_data['return']['markets'][coincall]['buyorders'][0]['price'])
        coin_dict['bestask'] = float(cryptsy_market_data['return']['markets'][coincall]['sellorders'][0]['price'])
    else: coin_dict['found'] = False
    return coin_dict

#print(cryptsy_coins())

##print(cryptsy("flap"))
##print(cryptsy("smc"))
##print(cryptsy("doge"))
