import urllib.request
import json

# bter has a depth type API  (along with btce and poloniex)

def bter_coins():
    coin_dict = {'found':True}
    bter_pairs_api = "http://data.bter.com/api/1/pairs"
    yawn = {'User-Agent' : 'minerjeff'}
    request = urllib.request.Request(bter_pairs_api, None, yawn)
    try: full = str(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
                print(e)
                print(bter_pairs_api)
                coin_dict = {'found':False}
                return coin_dict
    try: json_data = json.loads(full[4:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict

    for exchange in json_data:
        label = exchange.split('_')
        base = label[1].upper()
        coin = label[0].upper()
        if base in coin_dict.keys():
            coin_dict[base].append(coin)
        else:
            coin_dict[base] = [coin]

    return coin_dict

def bter(coin,base="btc",threshold=.001):
    coin_dict = {'found':True}
    tradepair = coin.lower() + '_' + base.lower()
    bter_order_api = 'http://data.bter.com/api/1/depth/' + str(tradepair)
    yawn = {'User-Agent' : 'minerjeff'}
    request = urllib.request.Request(bter_order_api, None, yawn)
    try: full = str(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
                print(e)
                print( bter_order_api + tradepair)
                coin_dict = {'found':False}
                return coin_dict
    #to get JSON, need to remove b' from beginning and ' from end
    #print (full)
    #json_data = json.loads(full)
    try: json_data = json.loads(full[4:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict

    if 'bids' in json_data.keys(): bestbid=0
    else:
        coin_dict['found'] = False
        return coin_dict
    bestbid = 0
    totalamount = 0
    for rate in json_data['bids']:
        rate[0] = float(rate[0])
        if rate[0] > bestbid:
            ## lets make sure it's not some silly small bid
            if ((rate[1]+totalamount)*rate[0]) < threshold:
                totalamount += rate[1] #count the amount to add to next bid
            else:
                bestbid=rate[0]
                totalamount = 0
    bestask = 1000000000
    totalamount = 0
    for rate in json_data['asks']:
        rate[0] = float(rate[0])
        if rate[0] < bestask:
            if((rate[1]+totalamount)*rate[0]) < threshold:
                totalamount += rate[1]
            else:
                bestask=rate[0]
                totalamount = 0

    if bestbid == 0:
        coin_dict['found'] = False
        return coin_dict
    else:
        coin_dict['bestbid'] = bestbid
        coin_dict['bestask'] = bestask
        return coin_dict

dict = bter('DOGE','BTC',10)

print ('bestbid: {:.8f}\n '.format(dict['bestbid']) + 'bestask: {:.8f}\n'.format(dict['bestask']))

#print(bter_coins())
