from BaseBot import BaseWaveMessageBot

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
        if 'No Content' in msg['body']:
            self.disconnect()
        elif 'Bad Request' in msg['body']:
            self.disconnect()
            print('ERROR: Bad Request')
            raise ValueError

    def post_message(self, url, value):
        self.set_message(url, value)
        self.run()
