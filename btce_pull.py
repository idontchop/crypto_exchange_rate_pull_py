import urllib.request
import hashlib
import hmac
import urllib.parse
import json

"""
Note, this is the easy way to get the current best bid and ask
calling /ticker will receive the "sell-now" and "buy-now" rates
basically just flip them to get Bid and Ask

Calling /depth will give better bid and ask information
"""

def btce(coin,base='btc'):
        
    yawn = {'User-Agent' : 'minerjeff'}

    tradepair = coin.lower() + "_" + base.lower()
    btc_api = 'https://www.btc-e.com/api/2/' + tradepair + '/ticker'

    coin_dict = {'found': True}
    request = urllib.request.Request(btc_api, None, yawn)
    try: full = str(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
        print(e)
        print(btc_api)
        coin_dict['found'] = False
        return coin_dict

    try: json_data = json.loads(full[2:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict
    json_data = json_data['ticker']
    coin_dict['bestask'] = float(json_data['buy'])
    coin_dict['bestbid'] = float(json_data['sell'])

    return coin_dict


#print (btce("ltc","btc"))
