import sys
import json

from utils import parse_on_off
from BaseBot import BaseWaveMessageBot

class StatusBot(BaseWaveMessageBot):
    current_temp = None
    set_point = None
    boiler_on = None

    def __init__(self, serial_number, access_code, password):
        super().__init__(serial_number, access_code, password, "GET /ecus/rrc/uiStatus HTTP /1.0\nUser-Agent: NefitEasy")

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

            # Decode the encrypted message
            data = self.decode(to_decode)

            # For some reason we have a load of null characters at the end
            # of the message, so strip these out
            data = data.replace(b'\x00', b'')

            # 'decode' from bytes to str, with UTF-8 encoding
            # (a different sort of 'decode' to above!)
            data = data.decode('utf-8')
            if len(data) > 0:
                self.data = json.loads(data)['value']
                #pprint(data)

                # Temperature set point (ie. temperature it is aiming for)
                self.set_point = float(self.data['TSP'])

                # Current measured temperature at thermostat
                self.current_temp = float(self.data['IHT'])

                # Is hot water on or off
                self.hot_water = parse_on_off(self.data['DHW'])

                # Program mode: 'manual' or 'clock'
                self.program_mode = self.data['UMD']

                # Temperature Override Duration
                self.temp_override_duration = float(self.data['TOD'])

                self.current_switch_point = float(self.data['CSP'])

                self.temp_override_on = parse_on_off(self.data['TOR'])

                self.holiday_mode = parse_on_off(self.data['HMD'])

                self.day_as_sunday = parse_on_off(self.data['DAS'])

                self.tomorrow_as_sunday = parse_on_off(self.data['TAS'])

                # Is the boiler on or off (ie. flame on or off)
                if self.data['BAI'] == 'No':
                    self.boiler_on = 0
                elif self.data['BAI'] == 'CH' or self.data['BAI'] == 'HW':
                    self.boiler_on = 1

                self.disconnect()

    def update(self):
        self.run()
