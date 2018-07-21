import urllib.request
import json

# vircurex seems pretty easy but will require two pulls since they seperate their bid and ask

def vircurex(coin,base='btc'):
    tradepair = 'base=' + coin.upper() + '&alt=' + base.upper()
    vircurex_orders_buy = 'https://api.vircurex.com/api/get_highest_bid.json?' + tradepair
    vircurex_orders_sell = 'https://api.vircurex.com/api/get_lowest_ask.json?' + tradepair
    
    yawn = {'User-Agent' : 'minerjeff'}
    coin_dict = {'found': True }
    #data = {'requestKey' : 890324809324}
    #post_data = json.dumps(data).encode('utf-8')

    request = urllib.request.Request(vircurex_orders_buy, None, yawn)
    full = str(urllib.request.urlopen(request).read())

    try: json_data = json.loads(full[2:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict

    bestbid = float(json_data['value'])
    coin_dict['bestbid'] = bestbid
    
    request = urllib.request.Request(vircurex_orders_sell, None, yawn)
    full = str(urllib.request.urlopen(request).read())

    try: json_data = json.loads(full[2:full.__len__()-1])
    except ValueError:
        coin_dict['found'] = False
        return coin_dict
    bestask = float(json_data['value'])
    coin_dict['bestask'] = bestask

    return coin_dict

#print(vircurex("ANC"))


