
{ 'btc-markets' :
  { 'flap':
    { 'cryptsy':
      { 'found':True,
        'bid':0.0,
        'bestask':0.0,
        }
      }
    }
  'ltc-markets' :
  { 'doge':
    { 'cryptsy':
      { 'found': True,
        'bestbid':0.0,
        'bestask':0.0
        }
      }
    }
  }

""" a simple set could determine which coins belonged in which market
and the above dictionary would be created in the program """

btc_markets_list = ['DOGE','LTC','ANC','FLAP']

""" another simple set determines which exchanges have which markets """

cryptsy_btc_markets_list = ['DOGE','LTC','ANC','FLAP']



coins = {
""" a dictionary where I can add and remove coins as needed
key will identifier for market such as flap-btc
each key will have a dictionary as a value
this dictionary will contain keys for each exchange
each exchange will have a dictionary that contains:
1. the identifier used to call API, 2.  best buy 3. best sell
"""
#flap:
'flap-btc':
 { 'cryptsy':
   { 'api': "FLAP\/BTC",
     'buy': 0, #need not define here
     'sell': 0
    }
   'coinex':
   { 'api': None
    }
 }
#smc
'smc-btc':
 { 'cryptsy':
   { 'api': "SMC\/BTC"}
   'coinex':
   { 'api': "80" }

'flap-ltc':
 {
