import datetime
import warnings

from html.parser import HTMLParser


class WexScraper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.message_id = None
        self.message_time = None
        self.message_user = None
        self.message_text = None
        self.messages = []

        self.in_message_a = False
        self.in_message_span = False

        self.dev_online = False
        self.support_online = False
        self.admin_online = False

    def handle_data(self, data):
        # Capture contents of <a> and <span> tags, which contain
        # the user ID and the message text, respectively.
        if self.in_message_a:
            self.message_user = data.strip()
        elif self.in_message_span:
            self.message_text = data.strip()

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            # Check whether this <p> tag has id="msgXXXXXXXX" and
            # class="chatmessage *"; if not, it doesn't contain a message.
            message_id = None
            for k, v in attrs:
                if k == 'id':
                    if v[:3] != 'msg':
                        return
                    message_id = v
                if k == 'class' and 'chatmessage' not in v:
                    return

            # This appears to be a message <p> tag, so set the message ID.
            # Other code in this class assumes that if self.messageId is None,
            # the tags being processed are not relevant.
            if message_id is not None:
                self.message_id = message_id
        elif tag == 'a':
            if self.message_id is not None:
                # Check whether this <a> tag has class="chatmessage" and a
                # time string in the title attribute; if not, it's not part
                # of a message.
                message_time = None
                for k, v in attrs:
                    if k == 'title':
                        message_time = v
                    if k == 'class' and v != 'chatmessage':
                        return

                if message_time is None:
                    return

                # This appears to be a message <a> tag, so remember the message
                # time and set the inMessageA flag so the tag's data can be
                # captured in the handle_data method.
                self.in_message_a = True
                self.message_time = message_time
            else:
                for k, v in attrs:
                    if k != 'href':
                        continue

                    # If the <a> tag for dev/support/admin is present, then
                    # they are online (otherwise nothing appears on the
                    # page for them).
                    if v == 'https://wex.nz/profile/1':
                        self.dev_online = True
                    elif v == 'https://wex.nz/profile/2':
                        self.support_online = True
                    elif v == 'https://wex.nz/profile/3':
                        self.admin_online = True
        elif tag == 'span':
            if self.message_id is not None:
                self.in_message_span = True

    def handle_endtag(self, tag):
        if tag == 'p' and self.message_id is not None:
            # exiting from the message <p> tag

            # check for invalid message contents
            if self.message_id is None:
                warnings.warn("Missing message ID")
            if self.message_user is None:
                warnings.warn("Missing message user")
            if self.message_time is None:
                warnings.warn("Missing message time")

            if self.message_text is None:
                # messageText will be None if the message consists entirely
                # of emoticons.
                self.message_text = ''

            # parse message time
            t = datetime.datetime.now()
            message_time = t.strptime(self.message_time, '%d.%m.%y %H:%M:%S')

            self.messages.append((self.message_id, self.message_user,
                                  message_time, self.message_text))
            self.message_id = None
            self.message_user = None
            self.message_time = None
            self.message_text = None
        elif tag == 'a' and self.message_id is not None:
            self.in_message_a = False
        elif tag == 'span':
            self.in_message_span = False


class ScraperResults(object):
    __slots__ = ('messages', 'dev_online', 'support_online', 'admin_online')

    def __init__(self):
        self.messages = None
        self.dev_online = False
        self.support_online = False
        self.admin_online = False

    def __getstate__(self):
        return dict((k, getattr(self, k)) for k in ScraperResults.__slots__)

    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)
