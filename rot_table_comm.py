from pyModbusTCP.client import ModbusClient
import ctypes
from time import sleep

class RotTableComm(object):
    """
    Class used to communicate with the Inphax rotary table from IEAv.

    The table's firmware is programmed in a PLC and communicates via modbus protocol, 
    via ethernel cable.
    """
    

    def __init__(self, host="192.168.1.1", port=502):
        """__init__ constructor

        Args:
            host: ip of rot table. Defaults to "192.168.1.1".
            port: port number of connection. Defaults to 502.
        """

        # rotary table fixed values
        self.max_acc = 10_000
        self.max_roll_vel = 20_000 
        self.max_yaw_vel = 50_000


        self.client = ModbusClient(host=host, port=port)
        if not self.client.open():
            print("Connection Failed!")
        self.client.close()
        return 200



    def write_register(self, address_reg: ctypes.c_int, reg_value: ctypes.c_int16):
        if not self.client.open():
            print("Connection failed!")
            
        # sleep(.1)
        self.client.write_single_register(address_reg, reg_value)
        self.client.close()

    # Primary functions
    # These functions are results from the reverse engineering and tests
    # on the PLC registers and its possible values.
    def stop_emergency(self, status=4): # @test
        """ 0: reset status  4: stop immediately """
        self.write_register(20, status)
        sleep(0.1)
        self.write_register(20, 0)

    def move_roll(self, status=0): # @test
        """ 0: off  1: on """
        self.write_register(22, status)
    
    def move_yaw(self, status=0):
        """ 0: off  1: on """
        self.write_register(24, status)

    def set_direction_roll(self, direction=0): # @test value 4
        """ 0: off  1: positive 2: negative """
        self.write_register(26, direction)

    def set_direction_yaw(self, direction=0):
        """ 0: off  1: positive 2: negative """
        self.write_register(28, direction)



    def set_roll_vel(self, vel=0):
        if abs(vel) > self.max_roll_vel:
            if vel > 0.0:
                vel = self.max_roll_vel
            else:
                vel = -self.max_roll_vel
        self.write_register(46, abs(vel*100))
        if vel > 0.0:
            self.set_direction_roll(1)
        elif vel < 0.0:
            self.set_direction_roll(2)
        else:
            self.set_direction_roll(0)



    def set_roll_acc(self, acc=None):
        if acc is None:
            acc = self.max_acc
        self.write_register(40, acc) # roll acceleration
        self.write_register(42, acc) # maximum roll acceleration


        
    def set_yaw_vel(self, vel=0):
        if abs(vel) > self.max_yaw_vel:
            if vel > 0.0:
                vel = self.max_yaw_vel
            else:
                vel = -self.max_yaw_vel
        self.write_register(56, abs(vel*100))
        if vel > 0.0:
            self.set_direction_yaw(1)
        elif vel <0.0:
            self.set_direction_yaw(2)
        else:
            self.set_direction_yaw(0)
            


    def set_yaw_acc(self, acc=None):
        if acc is None:
            acc = self.max_acc
        self.write_register(50, acc) # yaw acceleration
        self.write_register(52, acc) # maximum acceleration



    def stop(self): # @test
        """
            Non-emergencial stop.
        """
        self.move_roll(1)
        self.move_yaw(1)

        # stop roll movement
        self.set_direction_roll(0)
        self.set_roll_acc(self.max_acc)
        self.set_roll_vel(0)

        # stop yaw movement
        self.set_direction_yaw(0)
        self.set_yaw_acc(self.max_acc)
        self.set_yaw_vel(0)

        self.move_roll(0)
        self.move_yaw(0)
        


    def set_roll_position(self, pos:ctypes.c_int32, ensure_position=True):
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

    def jog_roll(self, vel=0, acc=None):
        if acc is None:
            acc = self.max_acc
        self.set_roll_vel(vel)
        self.set_roll_acc(acc)
        self.move_roll(1)

    
    def jog_yaw(self, vel=0, acc=None):
        if acc is None:
            acc = self.max_acc
        self.set_yaw_vel(vel)
        self.set_yaw_acc(acc)
        self.move_yaw(1)
        

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
    
    def set_yaw_velocity(self,vel :ctypes.c_int32):
        vel *= 100_0
        self.write_register(address_reg=22,reg_value=1)
        self.write_register(address_reg=24, reg_value=1)
        self.write_register(address_reg=0, reg_value=28)
        lower_velocity = -50000
        upper_velocity = 50000
        _clipped_vel = max(lower_velocity, min(upper_velocity, vel))
        _abs_clipped_vel = abs(_clipped_vel)
        _msb_pos = _abs_clipped_vel >> 16
        _lsb_pos = _abs_clipped_vel & 0xFFFF
        self.write_register(address_reg=56, reg_value=_lsb_pos)
        self.write_register(address_reg=57, reg_value=_msb_pos)
        if _clipped_vel < 0:
            # put on reverse mode
            self.write_register(address_reg=28,reg_value=2)
        else:
            self.write_register(address_reg=28, reg_value=1)
