#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   example.py
@Time    :   2024/03/22 00:12:15
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
'''
from rot_table_comm.rot_table_comm import RotTableComm 
rt = RotTableComm()
# to put rot table with roll in 45 degree and yaw with 90 degree with can do:
rt.set_roll_position(45)
rt.set_yaw_position(90)
