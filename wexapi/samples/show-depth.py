#!/usr/bin/env python
import sys
import pylab
import numpy as np

import wexapi

# If an argument is provided to this script, it will be interpreted
# as a currency pair for which depth should be displayed. Otherwise
# the BTC/USD depth will be displayed.

if len(sys.argv) >= 2:
    pair = sys.argv[1]
    print("Showing depth for %s" % pair)
else:
    print("No currency pair provided, defaulting to btc_usd")
    pair = "btc_usd"

api = wexapi.public.PublicApi(wexapi.common.WexConnection())

asks, bids = api.get_depth(pair)

print(len(asks), len(bids))

ask_prices, ask_volumes = zip(*asks)
bid_prices, bid_volumes = zip(*bids)

pylab.plot(ask_prices, np.cumsum(ask_volumes), 'r-')
pylab.plot(bid_prices, np.cumsum(bid_volumes), 'g-')
pylab.grid()
pylab.title("%s depth" % pair)
pylab.show()
