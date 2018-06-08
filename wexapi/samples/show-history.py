#!/usr/bin/env python
import sys
import matplotlib.pyplot as pyplot
import wexapi

# If an argument is provided to this script, it will be interpreted
# as a currency pair for which history should be displayed. Otherwise
# the BTC/USD history will be displayed.

if len(sys.argv) >= 2:
    pair = sys.argv[1]
    print("Showing history for %s" % pair)
else:
    print("No currency pair provided, defaulting to btc_usd")
    pair = "btc_usd"

conn = wexapi.common.WexConnection()
api = wexapi.public.PublicApi(connection=conn)
info = wexapi.public.InfoApi(connection=conn)
history = api.get_trade_history(pair, info)

print(len(history))

pyplot.plot(
    [t.timestamp for t in history if t.type == 'ask'],
    [t.price for t in history if t.type == 'ask'],
    'ro',
)

pyplot.plot(
    [t.timestamp for t in history if t.type == 'bid'],
    [t.price for t in history if t.type == 'bid'],
    'go',
)

pyplot.grid()
pyplot.show()
