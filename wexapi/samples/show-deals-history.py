#!/usr/bin/env python
from datetime import datetime
import sys
import wexapi

if len(sys.argv) < 2:
    print("Usage: compute-account-value.py <key file>")
    print("    key file - Path to a file containing key/secret/nonce data")
    sys.exit(1)

if len(sys.argv) >= 3:
    pair = sys.argv[2]
    print("Showing history for %s" % pair)
else:
    print("No currency pair provided, defaulting to btc_usd")
    pair = "btc_usd"

if len(sys.argv) >= 4:
    sort = sys.argv[3]
else:
    sort = "ASC"

print("Sorting: {}".format(sort))

key_file = sys.argv[1]
with wexapi.keyhandler.KeyHandler(key_file) as handler:
    if not handler.keys:
        print("No keys in key file.")
    else:
        for key in handler.keys:
            print("Computing value for key %s" % key)
            with wexapi.common.WexConnection() as conn:
                t = wexapi.trade.TradeApi(key, handler, connection=conn)

                try:
                    items = t.trade_history(pair=pair, count_number=10, order=sort)

                    print("Show last 10 deals")
                    for item in items:
                        utc_time = datetime.utcfromtimestamp(item.timestamp)
                        print("\tDate: {}".format(utc_time.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")))
                        print("\tType: {}".format(item.type))
                        print("\tOrder ID: {}".format(item.order_id))
                        print("\tDeal ID: {}".format(item.transaction_id))
                        print("\tIs my order: {}".format(item.is_your_order))
                        print()
                except Exception as e:
                    print("  An error occurred: %s" % e)
                    raise e
