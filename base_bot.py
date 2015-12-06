import sys
from pprint import pprint
import json

import sleekxmpp

from utils import decode, parse_on_off, create_message

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class BaseWaveMessageBot(sleekxmpp.ClientXMPP):
    current_temp = None
    set_point = None
    boiler_on = None

    def __init__(self, message):
        jid = "rrccontact_458921440@wa2-mz36-qrmzh6.bosch.de"
        password = "Ct7ZR03b_***REMOVED***"
        recipient = "rrcgateway_458921440@wa2-mz36-qrmzh6.bosch.de"
        #message = "GET /ecus/rrc/uiStatus HTTP /1.0\nUser-Agent: NefitEasy"

        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def connect(self):
        return sleekxmpp.ClientXMPP.connect(self, ('wa2-mz36-qrmzh6.bosch.de', 5222))

    def start(self, event):
        """
        Process the session_start event.

        Send a message to request the status
        """
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
