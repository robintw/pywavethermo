import sys
from pprint import pprint
import json

import sleekxmpp

from BaseBot import BaseWaveMessageBot


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class SetBot(BaseWaveMessageBot):
    current_temp = None
    set_point = None
    boiler_on = None

    def __init__(self, serial_number, access_code, password):
        super().__init__(serial_number, access_code, password, "")

    def message(self, msg):
        """
        Process a message once it has been received
        """
        print(msg)
        if 'No Content' in msg['body']:
            self.disconnect()
        elif 'Bad Request' in msg['body']:
            self.disconnect()
            print('ERROR: Bad Request')
            raise ValueError

    def post_message(self, url, value):
        self.set_message(url, value)
        print(self.msg)
        self.run()

if __name__ == '__main__':
    wave = SetBot(serial_number='458921440',
                  access_code='E6z5sHWaxiQYCwfU',
                  password='Elmer2301i')

    wave.set_message("/heatingCircuits/hc1/usermode", 'manual')
    wave.run()
