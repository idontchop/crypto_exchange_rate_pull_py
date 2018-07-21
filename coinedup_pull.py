import urllib.request
import json

# because coinex doesn't list the bid/ask on the market pull, will have to pull each coin
# easily changable but have to know the tradepair identifier

tradepair = 'BTC_FLAP'
coinedup_market_api = 'https://api.coinedup.com/markets'
google = 'https://www.google.com'

"""yawn = {'Content-Type': 'application/json',
           'Accept' : 'application/json',
           'User-Agent' : 'minerjeff'}"""
yawn = {'User-Agent' : 'minerjeff'}

data = {'requestKey' : 890324809324}
post_data = json.dumps(data).encode('utf-8')
print ("Loading: " + coinedup_market_api + " with " + str(data))
request = urllib.request.Request(coinedup_market_api, post_data, yawn)
full = str(urllib.request.urlopen(request).read())

print("Scraping beginning and end marks to get perfect json:\n\n")
#to get JSON, need to remove b' from beginning and ' from end

print(full)

#json_data = json.loads(full[2:full.__len__()-1])


"""
# coinex is going to be funky I guess, will have to loop through and count the bids

bestbid = 0
for rate in json_data['orders']:
    if rate['bid'] == True and rate['filled'] < rate['amount']:
        if rate['rate'] > bestbid: bestbid = rate['rate']
        print("{:.8f}".format(rate['rate'] * .00000001), " ", rate['amount']*.00000001, (rate['amount'] - rate['filled'])*.00000001)

# for now just do a simple copy and past to get asks
print("\nbegin ask:\n\n")
count = 0
bestask = 10000000
for rate in json_data['orders']:
    need to see if it is ask and if it is filled, if it is a bid and not filled, then print
    will also multiple by one satoshi to fix coinex's delivery of positive numbers (purely for visual reasons)
    will also see if there is a different between amount and filled
    #only show ten
    if rate['bid'] == False and rate['filled'] < rate['amount']:
        if rate['rate'] < bestask: bestask = rate['rate']
        count+=1
        if count == 10:break
        print("{:.8f}".format(rate['rate'] * .00000001), " ", rate['amount']*.00000001, " ", (rate['amount'] - rate['filled'])*.00000001)

bestbid *= .00000001
bestask *= .00000001
print("\nBest Bid: ", bestbid, "   Best Ask: ", bestask)

reference from cryptsy file
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

"""
