from pyModbusTCP.client import ModbusClient
import ctypes
from time import sleep

class RotTableComm(object):
    """docstring for RotTableComm."""

    def __init__(self, host="192.168.1.1", port=502):
        """__init__ constructor

        Args:
            host: ip of rot table. Defaults to "192.168.1.1".
            port: port number of connection. Defaults to 502.
        """
        self.client = ModbusClient(host=host, port=port)
        if not self.client.open():
            print("Fail to open connection")
        self.client.close()
        # ge current states
        self.get_roll_position()
        self.get_roll_velocity()
        self.get_yaw_position()
        self.get_yaw_velocity()

    def write_register(self, address_reg: ctypes.c_int, reg_value: ctypes.c_int16):
        if not self.client.open():
            print('fail to open')

        # sleep(.1)
        self.client.write_single_register(address_reg, reg_value)
        self.client.close()

    def set_roll_position(self, pos:ctypes.c_int32,ensure_position=True):
        """set_roll_position

        Args:
            pos: angle of roll  in degrees. Defaults to ctypes.c_int32.
        """
        _pos = pos * 1_000
        if _pos < 0:
            _pos = 360_000 - abs(_pos)

        self.write_register(address_reg=22, reg_value=2) # IMPORTANT: probably this registrar abilisates the position of position control 
        self.write_register(address_reg=26, reg_value=0)
        # split _pos values of 32 bits in two 16 bits to write on register
        _msb_pos = _pos >> 16
        _lsb_pos = _pos & 0xFFFF
        self.write_register(address_reg=60, reg_value=_lsb_pos)
        self.write_register(address_reg=61, reg_value=_msb_pos)
        sleep(0.1)
        self.write_register(address_reg=26, reg_value=0)
        sleep(0.1)
        self.write_register(address_reg=26, reg_value=4)
        # update position variable
        
        self.roll_position = self.get_roll_position()
        # Check that the table is in the requested position
        if ensure_position:
            while abs(self.roll_position - pos) > 1:
                sleep(2)    
                self.set_roll_position(pos=pos, ensure_position=False)

    def set_yaw_position(self, pos:ctypes.c_int32, ensure_position=False):
        """set_yaw_position

        Args:
            pos: yaw position in degree. Defaults to ctypes.c_int32.
        """
        _pos = pos * 1_000
        if _pos < 0:
            _pos = 360_000 - abs(_pos)
        self.write_register(address_reg=24, reg_value=2)
        self.write_register(address_reg=28, reg_value=0)
        # split _pos values of 32 bits in two 16 bits to write on register
        _msb_pos = _pos >> 16
        _lsb_pos = _pos & 0xFFFF
        self.write_register(address_reg=70, reg_value=_lsb_pos)
        self.write_register(address_reg=71, reg_value=_msb_pos)
        self.write_register(address_reg=28, reg_value=0)
        sleep(0.1)
        self.write_register(address_reg=28, reg_value=4)  
        sleep(0.1)
        # update position variable
        self.yaw_position = self.get_yaw_position()
        # Check that the table is in the requested position
        if ensure_position:
            while abs(self.yaw_position-pos)>1:
                self.set_yaw_position(pos=pos,ensure_position=False)
                sleep(2)

    def get_yaw_position(self):
        _pos_list = self.client.read_input_registers(0, 2)
        self.yaw_position = (((_pos_list[1] << 16) + _pos_list[0])) / 1_000_000
        return self.yaw_position
    def get_yaw_velocity(self):
        _pos_list = self.client.read_input_registers(2, 2)
        self.yaw_velocity = (((_pos_list[1] << 16) + _pos_list[0])) / 1_000_000
        return self.yaw_velocity

    def get_roll_position(self):
        _pos_list = self.client.read_input_registers(4, 2)
        self.roll_position = (((_pos_list[1] << 16) + _pos_list[0])) / 1_000_000
        return self.roll_position

    def get_roll_velocity(self):
        _pos_list = self.client.read_input_registers(6, 2)
        self.roll_velocity = (((_pos_list[1] << 16) + _pos_list[0])) / 1_000_000
        return self.roll_velocity
    def go_home(self):
        self.set_roll_position(0)
        self.set_yaw_position(0)