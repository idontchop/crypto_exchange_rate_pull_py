import urllib.request
import json

cryptsy_market_api = 'http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=165'
google = 'http://www.google.com'

print (cryptsy_market_api)
full = str(urllib.request.urlopen(cryptsy_market_api).read())

print("Scraping beginning and end marks to get perfect json:\n\n")
#to get JSON from cryptsy, need to remove b' from beginning and ' from end

json_data = json.loads(full[2:full.__len__()-1])
##end testing get json
##Now to get the current buy

#print(json_data)

#lets test dicts

##shwew
print(json_data['return']['markets']['FLAP']['sellorders'][0]['price'])
##so, the following should find the current best buy and best sell?
##will it always be the first in the list?

bestbuy = json_data['return']['markets']['FLAP']['buyorders'][0]['price'];
bestsell = json_data['return']['markets']['FLAP']['sellorders'][0]['price'];
totalbuy = json_data['return']['markets']['FLAP']['buyorders'][0]['total'];
totalsell = json_data['return']['markets']['FLAP']['sellorders'][0]['total'];

print("bestbuy = ", bestbuy, totalbuy)
print("bestsell = ", bestsell, totalsell)

