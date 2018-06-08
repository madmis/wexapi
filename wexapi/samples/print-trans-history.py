#!/usr/bin/env python
import sys

import wexapi

if len(sys.argv) < 2:
    print("Usage: print-trans-history.py <key file>")
    print("    key file - Path to a file containing key/secret/nonce data")
    sys.exit(1)

key_file = sys.argv[1]
# NOTE: In future versions, resaveOnDeletion will default to True.
with wexapi.keyhandler.KeyHandler(key_file) as handler:
    if not handler.keys:
        print("No keys in key file.")
    else:
        for key in handler.keys:
            print("Printing info for key %s" % key)

            with wexapi.common.WexConnection() as conn:
                t = wexapi.trade.TradeApi(key, handler, connection=conn)

                try:
                    th = t.trans_history()
                    for h in th:
                        print("\t\t        id: %r" % h.transaction_id)
                        print("\t\t      type: %r" % h.type)
                        print("\t\t    amount: %r" % h.amount)
                        print("\t\t  currency: %r" % h.currency)
                        print("\t\t      desc: %s" % h.desc)
                        print("\t\t    status: %r" % h.status)
                        print("\t\t timestamp: %r" % h.timestamp)
                        print()
                except Exception as e:
                    print("  An error occurred: %s" % e)
