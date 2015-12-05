import sys
import json

import sleekxmpp

from utils import decode

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class WaveMessageBot(sleekxmpp.ClientXMPP):
    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """
    current_temp = None
    set_point = None
    boiler_on = None

    def __init__(self):
        jid = "rrccontact_458921440@wa2-mz36-qrmzh6.bosch.de"
        password = "Ct7ZR03b_E6z5sHWaxiQYCwfU"
        recipient = "rrcgateway_458921440@wa2-mz36-qrmzh6.bosch.de"
        message = "GET /ecus/rrc/uiStatus HTTP /1.0\nUser-Agent: NefitEasy"

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

    def message(self, msg):
        """
        Process a message once it has been received
        """
        spl = str(msg['body']).split("\n\n")

        if len(spl) < 2:
            # Invalid message
            return
        else:
            to_decode = spl[1].strip()
            data = decode(to_decode)
            data = data.replace(b'\x00', b'')
            data = data.decode('utf-8')
            if len(data) > 0:
                data = json.loads(data)['value']
                #print 'Current Set Point', data['TSP']
                set_point = data['TSP']
                #print 'Current temperature', data['IHT']
                current_temp = data['IHT']
                if data['BAI'] == 'No':
                    boiler_on = 0
                    #print 'Boiler off'
                elif data['BAI'] == 'CH':
                    boiler_on = 1
                    #print 'Boiler on',

                #print("%s,%s,%s,%s" % (data['CTD'], current_temp, set_point, boiler_on))

                self.current_temp = current_temp
                self.set_point = set_point
                self.boiler_on = boiler_on

                self.disconnect()

if __name__ == '__main__':
    wave = WaveMessageBot()

    # Connect to the Bosch XMPP server and start processing messages
    if wave.connect():
        wave.process(block=True)
        print(wave.set_point, wave.current_temp, wave.boiler_on)
    else:
        print("Unable to connect.")
