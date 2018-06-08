#!/usr/bin/env python
import sys
import wexapi

if len(sys.argv) < 2:
    print("Usage: compute-account-value.py <key file>")
    print("    key file - Path to a file containing key/secret/nonce data")
    sys.exit(1)

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
                    r = t.get_info()

                    exchange_rates = {}
                    for pair in t.apiInfo.pair_names:
                        asks, bids = wexapi.public.PublicApi(connection=conn).get_depth(pair)
                        exchange_rates[pair] = bids[0][0]

                    btc_total = 0
                    for currency in t.apiInfo.currencies:
                        balance = r.funds[currency]
                        if currency == "btc":
                            print("\t%s balance: %s" % (currency.upper(), balance))
                            btc_total += balance
                        else:
                            pair = "%s_btc" % currency
                            if pair in t.apiInfo.pair_names:
                                btc_equiv = balance * exchange_rates.get(pair, 1)

                                bal_str = t.apiInfo.format_currency(pair, balance)
                                btc_str = t.apiInfo.format_currency("btc_usd", btc_equiv)
                                print("\t%s balance: %s (~%s BTC)" % (currency.upper(),
                                                                      bal_str, btc_str))
                                btc_total += btc_equiv

                    print("\tCurrent value of open orders:")
                    orders = t.active_orders()
                    if orders:
                        for o in orders:
                            c1, c2 = o.pair.split("_")
                            c2_equiv = o.amount * exchange_rates.get(o.pair, 1)
                            if c2 == "btc":
                                btc_equiv = c2_equiv
                            else:
                                btc_equiv = c2_equiv / exchange_rates.get("btc_{}".format(c2), 1)

                            btc_str = t.apiInfo.format_currency(o.pair, btc_equiv)
                            print("\t\t%s %s %s @ %s (~%s BTC)" % (o.type, o.amount,
                                                                   o.pair, o.rate,
                                                                   btc_str))
                            btc_total += btc_equiv
                    else:
                        print("\t\tThere are no open orders.")

                    btc_str = t.apiInfo.format_currency("btc_usd", btc_total)
                    print("\n\tTotal estimated value: %s BTC" % btc_str)
                    for fiat in ("usd", "eur", "rur"):
                        fiat_pair = "btc_%s" % fiat
                        fiat_total = btc_total * exchange_rates.get(fiat_pair, 1)
                        fiat_str = wexapi.utils.format_currency_digits(fiat_total, 2)
                        print("\t                       %s %s" % (fiat_str,
                                                                  fiat.upper()))

                except Exception as e:
                    print("  An error occurred: %s" % e)
                    raise e
