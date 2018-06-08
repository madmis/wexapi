#!/usr/bin/env python
import wexapi

attrs = ('high', 'low', 'avg', 'vol', 'vol_cur', 'last', 'buy', 'sell', 'updated')

print("Tickers:")
connection = wexapi.common.WexConnection()
info = wexapi.public.InfoApi(connection)
api = wexapi.public.PublicApi(connection)
for pair in info.pair_names:
    ticker = api.get_ticker(pair, info)
    print(pair)
    for a in attrs:
        print("\t%s %s" % (a, getattr(ticker, a)))
