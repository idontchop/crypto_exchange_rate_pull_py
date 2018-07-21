import urllib.request
import json

coinse_market_data = {}

def coinse(coin,base="btc",threshold=.001):
    """ coins-e has a depth pull with its market pull
    In the asks/bids list
    "n": denotes number of open orders
    "r": denotes rate (in terms of C2)
    "q": denotes quantity on offer (in terms of C1)
    "cq": denotes cummulative quantity, i.e total quantity available at this rate (in terms of C1)
    """
    tradepair = coin.upper() + '_' + base.upper()
    coin_dict = {'found':True}
    coinse_market_api = 'https://www.coins-e.com/api/v2/markets/data/'
    #coinse_order_api = 'https://www.coins-e.com/api/v2/market/' + str(tradepair) + '/depth/'
    
    """yawn = {'Content-Type': 'application/json',

           'Accept' : 'application/json',
           'User-Agent' : 'minerjeff'}"""
    yawn = {'User-Agent' : 'minerjeff'}
    global coinse_market_data
    if  'markets' in coinse_market_data:
        #do nothing
        coin_dict['found'] = True
    else:
        """if coinse_data isn't filled, need to query"""
        request = urllib.request.Request(coinse_market_api, None, yawn)
        try: full = str(urllib.request.urlopen(request).read())
        except urllib.error.HTTPError as e:
                print(e)
                print(tradepair)
                coin_dict = {'found':False}
                return coin_dict
        #to get JSON, need to remove b' from beginning and ' from end
        try: coinse_market_data = json.loads(full[2:full.__len__()-1])
        except ValueError:
            print("json error in coinse")
            coin_dict['found'] = False
            return coin_dict
    if not tradepair in coinse_market_data['markets']:
        print(tradepair + " not found at coins-e")
        coin_dict['found'] = False
        return coin_dict
    bestbid = 0
    totalamount = 0
    for rate in coinse_market_data['markets'][tradepair]['marketdepth']['bids']:
        rate['r'] = float(rate['r'])
        rate['cq'] = float(rate['cq'])
        if rate['r'] > bestbid:
            if ((rate['cq']+totalamount)*rate['r']) < threshold:
                totalamount += rate['cq']
            else:
                bestbid=rate['r']
                totalamount = 0
       
    bestask = 1000000000
    for rate in coinse_market_data['markets'][tradepair]['marketdepth']['asks']:
        rate['r'] = float(rate['r'])
        rate['cq'] = float(rate['cq'])
        if rate['r'] < bestask:
            if ((rate['cq']+totalamount)*rate['r']) < threshold:
                totalamount += rate['cq']
            else:
                bestask = rate['r']
                totalamount = 0
    
    if bestbid == 0: #oops must have not found the tradepair
        coin_dict['found']=False
    else: coin_dict['found']=True
    coin_dict['bestbid'] = bestbid
    coin_dict['bestask'] = bestask
    return coin_dict

#dict = coinse('bet','btc',.05)
#print ('bestbid: {:.8f}\n '.format(dict['bestbid']) + 'bestask: {:.8f}\n'.format(dict['bestask']))
