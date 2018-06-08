#!/usr/bin/env python
import wexapi

with wexapi.common.WexConnection() as connection:
    info = wexapi.public.InfoApi(connection)

    mainPage = info.scrape_main_page()
    for message in mainPage.messages:
        msgId, user, time, text = message
        print("%s %s: %s" % (time, user, text))

    print()

    print("dev online: %s" % ('yes' if mainPage.dev_online else 'no'))
    print("support online: %s" % ('yes' if mainPage.support_online else 'no'))
    print("admin online: %s" % ('yes' if mainPage.admin_online else 'no'))
