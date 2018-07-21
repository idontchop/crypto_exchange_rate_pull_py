import urllib.request
import json

# mintpal will require two pulls since they seperate their bid and ask

def mintpal_coins():
        coin_dict = {'found': True }
        mintpal_summary_api = 'https://api.mintpal.com/market/summary/' 
        yawn = {'User-Agent' : 'minerjeff'}
        request = urllib.request.Request(mintpal_summary_api, None, yawn)
        try: full = str(urllib.request.urlopen(request).read())
        except urllib.error.HTTPError as e:
                print(e)
                print(tradepair)
                coin_dict = {'found':False}
                return coin_dict

        try: json_data = json.loads(full[2:full.__len__()-1])
        except ValueError:
                coin_dict['found'] = False
                return coin_dict

        for market in json_data:
                if market['exchange'] in coin_dict.keys():
                        coin_dict[market['exchange']].append(market['code'])
                else:
                        coin_dict[market['exchange']] = [market['code']]

        return coin_dict

        
def mintpal(coin,base='btc'):
        tradepair = coin.upper() + '/' + base.upper()
        mintpal_orders_buy = 'https://api.mintpal.com/market/orders/' + tradepair + '/BUY'
        mintpal_orders_sell = 'https://api.mintpal.com/market/orders/' + tradepair + '/SELL'
        """yawn = {'Content-Type': 'application/json',
                   'Accept' : 'application/json',
                   'User-Agent' : 'minerjeff'}"""
        yawn = {'User-Agent' : 'minerjeff'}

        coin_dict = {'found':True}
        #data = {'requestKey' : 890324809324}
        #post_data = json.dumps(data).encode('utf-8')

        request = urllib.request.Request(mintpal_orders_buy, None, yawn)
        try: full = str(urllib.request.urlopen(request).read())
        except urllib.error.HTTPError as e:
                print(e)
                print(tradepair)
                coin_dict = {'found':False}
                return coin_dict

        try: json_data = json.loads(full[2:full.__len__()-1])
        except ValueError:
                coin_dict['found'] = False
                return coin_dict
        # mintpal should be similar to coinex, will have to loop through and count the bids
        bestbid = 0
        for rate in json_data['orders']:
                rate['price'] = float(rate['price'])
                if rate['price'] > bestbid: bestbid = rate['price']

        coin_dict['bestbid'] = bestbid
        
        request = urllib.request.Request(mintpal_orders_sell, None, yawn)
        try: full = str(urllib.request.urlopen(request).read())
        except urllib.error.HTTPError as e:
                print(e)
                print(tradepair)
                coin_dict = {'found':False}
                return coin_dict
        try: json_data = json.loads(full[2:full.__len__()-1])
        except ValueError:
                coin_dict['found'] = False
                return coin_dict

        bestask=100000000
        for rate in json_data['orders']:
                rate['price'] = float(rate['price'])
                if rate['price'] < bestask: bestask = rate['price']

        coin_dict['bestask'] = bestask

        return coin_dict

#print(mintpal("doge"))
#print(mintpal_coins())
