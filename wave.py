import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
#logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
import graphitesend

import hashlib
import base64
from Crypto.Cipher import AES
from lxml import objectify
import json
import os

from wave import decode

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input



class SendMsgBot(sleekxmpp.ClientXMPP):

    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """
    current_temp = None
    set_point = None
    boiler_on = None

    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        #self.disconnect(wait=True)

    def message(self, msg):
        spl = str(msg['body']).split("\n\n")
        if len(spl) < 2:
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

                print("%s,%s,%s,%s" % (data['CTD'], current_temp, set_point, boiler_on))

                self.current_temp = current_temp
                self.set_point = set_point
                self.boiler_on = boiler_on

                self.disconnect()

if __name__ == '__main__':
    jid = "rrccontact_458921440@wa2-mz36-qrmzh6.bosch.de"
    password = "Ct7ZR03b_E6z5sHWaxiQYCwfU"
    to = "rrcgateway_458921440@wa2-mz36-qrmzh6.bosch.de"
    message = "GET /ecus/rrc/uiStatus HTTP /1.0\nUser-Agent: NefitEasy"

    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = SendMsgBot(jid, password, to, message)
    
    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect(('wa2-mz36-qrmzh6.bosch.de', 5222)):
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print(xmpp.set_point, xmpp.current_temp, xmpp.boiler_on)
        #os.system('mysql -u robin --password=timothy heating -e "INSERT INTO data (set_point, temp, boileron, lounge_temp) VALUES (%s, %s, %s, %f);"' % (xmpp.set_point, xmpp.current_temp, xmpp.boiler_on, lounge_temp))
        #graphitesend.init(graphite_server='localhost', system_name='', group='boiler', prefix='house')
        #graphitesend.send_dict({'setpoint':xmpp.set_point, 'current_temp':xmpp.current_temp, 'boiler_on':xmpp.boiler_on})
    else:
        print("Unable to connect.")
