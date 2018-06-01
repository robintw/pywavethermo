import base64
from Crypto.Cipher import AES

import sleekxmpp

import ssl

from utils import get_md5

class BaseWaveMessageBot(sleekxmpp.ClientXMPP):

    secret = b'X\xf1\x8dp\xf6g\xc9\xc7\x9e\xf7\xdeC[\xf0\xf9\xb1U;\xbbna\x81b\x12\xab\x80\xe5\xb0\xd3Q\xfb\xb1'


    def __init__(self, serial_number, access_code, password, message):

        jid = "rrccontact_%s@wa2-mz36-qrmzh6.bosch.de" % serial_number
        connection_password = "Ct7ZR03b_%s" % access_code

        sleekxmpp.ClientXMPP.__init__(self, jid, connection_password)

        self.recipient = "rrcgateway_%s@wa2-mz36-qrmzh6.bosch.de" % serial_number
        self.msg = message

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        self.connected = False

        abyte1 = get_md5(access_code.encode() + self.secret)
        abyte2 = get_md5(self.secret + password.encode())

        self.key = abyte1 + abyte2

    def connect(self):
        self.connected = True
        return sleekxmpp.ClientXMPP.connect(self, ('wa2-mz36-qrmzh6.bosch.de', 5222),
                                            use_ssl=False,
                                            use_tls=False)

    def disconnect(self):
        self.connected = False
        return sleekxmpp.ClientXMPP.disconnect(self)

    def run(self):
        self.connect()
        self.go()
        self.process(block=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def go(self):
        if not self.connected:
            self.connect()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

    ##
    ## Now functions for encoding/decoding and creating messages
    ##
    def set_message(self, url, value):
        j = '{"value":%s}' % (repr(value))

        remainder = len(j) % 16

        j = j + '\x00' * (16 - remainder)

        self.msg = "PUT %s HTTP:/1.0\nContent-Type: application/json\nContent-Length: 25\nUser-Agent: NefitEasy\n\n\n\n%s\n" % (url, self.encode(j).decode('utf-8'))

    def encode(self, s):
        a = AES.new(self.key)
        a = AES.new(self.key, AES.MODE_ECB)
        res = a.encrypt(s)

        encoded = base64.b64encode(res)

        return encoded

    def decode(self, data):
        decoded = base64.b64decode(data)

        a = AES.new(self.key)
        a = AES.new(self.key, AES.MODE_ECB)
        res = a.decrypt(decoded)

        return res
