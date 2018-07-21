import cryptsymarketpull
import time

count = 0
coin = cryptsymarketpull.cryptsy("flap")
if coin['found'] == True: print ("Flap best bid is: {:.8f}".format(coin['bestbid']))
coin = cryptsymarketpull.cryptsy("doge")
if coin['found'] == True: print ("Doge best bid is: {:.8f}".format(coin['bestbid']))
coin = cryptsymarketpull.cryptsy("smc")
if coin['found'] == True: print ("Smc best bid is: {:.8f}".format(coin['bestbid']))
time.sleep(1)
input("Press any key and hit enter:")
