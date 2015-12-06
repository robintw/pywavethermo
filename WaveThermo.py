from SetBot import SetBot
from StatusBot import StatusBot

class WaveThermo:

    def __init__(self, serial_number, access_code, password):
        self.status = StatusBot(serial_number=serial_number,
                                access_code=access_code,
                                password=password)

        self.setter = SetBot(serial_number=serial_number,
                             access_code=access_code,
                             password=password)

    def set_mode(self, mode):
        """
        Set the control mode of the thermostat

        Parameters
        ----------
        mode : str
            Control mode, either "manual" or "clock"
        """
        self.setter.post_message("/heatingCircuits/hc1/usermode", mode)

    def set_temperature(self, temperature):
        self.status.update()

        if self.status.program_mode == 'manual':
            self.setter.post_message("/heatingCircuits/hc1/temperatureRoomManual", temperature)
        else:
            self.setter.post_message("/heatingCircuits/hc1/manualTempOverride/temperature", temperature)
            self.setter.post_message("/heatingCircuits/hc1/manualTempOverride/status", 'on')

    def override(self, b):
        print('in override')
        if b:
            self.setter.post_message("/heatingCircuits/hc1/manualTempOverride/status", 'on')
        else:
            self.setter.post_message("/heatingCircuits/hc1/manualTempOverride/status", 'off')
