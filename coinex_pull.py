import urllib.request
import json

# because coinex doesn't list the bid/ask on the market pull, will have to pull each coin
# easily changable but have to know the tradepair identifier
# to get trade pair identifier, we will simply pull their trade_pairs api every time.  Their fault...

trade_pairs = { 'found': False }
def get_trade_pair_id(coin,base='btc'):
    """This will first look if trade_pairs{} is defined
    if not, it will query coinex for the trade pair json and update trade_pairs
    Then it will search trade_pairs for the coin arguments and return the identifier"""
    slug = coin.lower() + "_" + base.lower()
    trade_pairs_api = "https://coinex.pw/api/v2/trade_pairs"
    yawn = {'Content-Type': 'application/json',
           'Accept' : 'application/json',
           'User-Agent' : 'minerjeff'}
    if trade_pairs['found'] == False:
        """build trade_pairs{}, this should only be done once in a run"""
        request = urllib.request.Request(trade_pairs_api, None, yawn)
        try: full = str(urllib.request.urlopen(request).read())
        except urllib.error.HTTPError as e:
                print(e)
                coin_dict = {'found':False}
                return coin_dict

        try: json_data = json.loads(full[2:full.__len__()-1])
        except ValueError:
            #hmm, this sucks, gonna have to not get coinex at all
            return -1
        ## now lets build trade_pairs for later calls
        for pair in json_data['trade_pairs']:
            trade_pairs[pair['url_slug']] = pair['id']
        #everything seems good, change found
        trade_pairs['found'] = True

    #wow easy lol
    if slug in trade_pairs:
        return trade_pairs[slug]
    else: return -1
    

def coinex(coin,base='btc'):
    """ coinex has an identifier for each trade_pair which will have to be found first
    afterwards, it's a fairly easy call to a depth type API
    """
    tradepair = get_trade_pair_id(coin,base)
    coinex_api = 'http://coinex.pw/api/v2/orders?tradePair=' + str(tradepair)
    yawn = {'Content-Type': 'application/json',
           'Accept' : 'application/json',
           'User-Agent' : 'minerjeff'}
    coin_dict = {'found':True}
    request = urllib.request.Request(coinex_api, None, yawn)
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

    bestbid = 0
    for rate in json_data['orders']:
        if rate['bid'] == True and rate['filled'] < rate['amount']:
            if rate['rate'] > bestbid: bestbid = rate['rate']

    bestask = 10000000
    for rate in json_data['orders']:
        if rate['bid'] == False and rate['filled'] < rate['amount']:
            if rate['rate'] < bestask: bestask = rate['rate']

    #coinex just wants to be different
    bestbid *= .00000001
    bestask *= .00000001
    coin_dict['bestbid'] = bestbid
    coin_dict['bestask'] = bestask

    return coin_dict

#print(coinex("doge"))
    
