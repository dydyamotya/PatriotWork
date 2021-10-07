import typing

from pymodbus.client.sync import ModbusSerialClient


class GasMixException(Exception):
    pass


class GasMix:
    def __init__(self, port: typing.Optional[str], unit_num: int):
        self.port = port
        try:
            self.ser = ModbusSerialClient(port=self.port, method="rtu", baudrate=19200)
        except Exception as e:
            raise GasMixException(e)
        else:
            self.unit = unit_num

    def open_valve(self, valve_number: int):
        self.ser.write_coil(valve_number, 0xFF00, unit=self.unit)

    def open_valve_close_others(self, valve_number: int):
        values = [0, ] * 8
        values[valve_number] = 1
        self.ser.write_coils(0x0000, values=values, unit=self.unit)

    def close_all_valves(self):
        self.ser.write_coils(0x0000, values=(0,) * 8, unit=self.unit)

    def set_port(self, port: str):
        self.ser.port = port
