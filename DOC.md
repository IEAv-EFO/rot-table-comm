Addresses to control rotary table from IEAv
PLC is connected through modbus protocol 
192.168.1.1 port 502

The idea is to avoid the compilation of the original code in C, that is cumbersome when dealing with different systems.
It requires the modbus compilation, the mongoose server, the javascript application, all that system that came with the table.
Instead, we can simply use a python package to communicate using modbusTCP library. 

All velocities and positions must be entered as engineering units multiplied by 100: input_variable = ang_vel*100

The commands in the c library opens and closes the modbus connection for each communication

Movement control

	20:		emergency stop
			4 - stop
			0 - reset to normal

			reset function:	write 1, then 0, then 1, then 0.
			after config: write 2, then 0.

	22:		pitch and yaw movement
			0 - off
			1 - on
			2 - backward?

	24: 	yaw movement??? 	% something is missing from this command, it is not the same as #28
			0 - off
			1 - on

	26:		pitch movement	
			0 - off
			1 - on forward	
			2 - on backward

	28: 	yaw movement
			0 - off
			1 - on forward
			2 - on backward
			4 - ?

			after position control
			send 0, then 4.


Setting configuration values

some addresses, for example 46 and 56, receives a 32 bit integer value and must be written in two registers.
code example:
		uint16_t regs[2];
		regs[0] = valor & 0x0000FFFF;
		regs[1] = valor >> 16; 
		modbus_write_registers(ctx, endereco, 1, &regs[0]); % equivalent to write_multiple_registers() from modbusTCP in python
		modbus_write_registers(ctx, endereco + 1, 1, &regs[1]);


	40:		pitch acceleration position
	
	42:		pitch max acceleration

	46:		pitch velocity	%using write_regs()

	50:		yaw acceleration position?
	
	52:		yaw maximum acceleration
	
	56: 	yaw velocity	%using write_regs()


	60: 	pitch position			%using write_regs()

	62:		pitch velocity position

	64:		pitch acceleration position

	70:		yaw position			%using write_regs()

	72: 	yaw velocity position

	74:		yaw acceleration position

	76:		yaw acceleration position

	80:		pitch max velocity

	82:		pitch max acceleration

	90:		yaw max velocity

	92:		yaw max acceleration







