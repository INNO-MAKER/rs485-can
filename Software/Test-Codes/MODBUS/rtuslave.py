#################################################################################################

## Description :  This codes is for test the Modbus communication
##                via RS485 function on 485&CAM module from innom-maker     
##                Set one RS485 port as master and the other as slave.
##                master can read data and control the slave.

## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.11.25

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                SYstem of RPI       ----------------------  2019-09-26-raspbian-buster-full
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

## To install dependencies:
## sudo pip3 install modbus-tk
##################################################################################################

import sys

import serial
import fcntl
import os
import struct
import termios
import array
import time

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
#import modbus_tk.modbus_rtu as modbus_rtu
from modbus_tk import modbus_rtu
# RS485 ioctls
TIOCGRS485 = 0x542E
TIOCSRS485 = 0x542F
SER_RS485_ENABLED = 0b00000001
SER_RS485_RTS_ON_SEND = 0b00000010
SER_RS485_RTS_AFTER_SEND = 0b00000100
SER_RS485_RX_DURING_TX = 0b00010000
# rs 485 port
ser1 = serial.Serial("/dev/ttySC0",9600)    
ser2 = serial.Serial("/dev/ttySC1",9600)

def rs485_enable():
    buf = array.array('i', [0] * 8) # flags, delaytx, delayrx, padding
    #enable 485 chanel 1
    fcntl.ioctl(ser1, TIOCGRS485, buf)
    buf[0] |=  SER_RS485_ENABLED|SER_RS485_RTS_AFTER_SEND
    buf[1]  = 0
    buf[2]  = 0
    fcntl.ioctl(ser1, TIOCSRS485, buf)

    #enable 485 chanel 2
    fcntl.ioctl(ser2, TIOCGRS485, buf)
    buf[0] |=  SER_RS485_ENABLED|SER_RS485_RTS_AFTER_SEND
    buf[1]  = 0
    buf[2]  = 0
    fcntl.ioctl(ser2, TIOCSRS485, buf)
#end of def rs485_enable():
       

if __name__ == '__main__':
    
    logger = modbus_tk.utils.create_logger("console")

    rs485_enable()
   
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    #Create the server
    server = modbus_rtu.RtuServer(serial.Serial('/dev/ttySC1'))

    try:
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")

        server.start()

        slave_1 = server.add_slave(1)
        slave_1.add_block('0', cst.HOLDING_REGISTERS, 0, 100)
        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break

            elif args[0] == 'add_slave':
                slave_id = int(args[1])
                server.add_slave(slave_id)
                sys.stdout.write('done: slave %d added\r\n' % (slave_id))

            elif args[0] == 'add_block':
                slave_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])
                slave = server.get_slave(slave_id)
                slave.add_block(name, block_type, starting_address, length)
                sys.stdout.write('done: block %s added\r\n' % (name))

            elif args[0] == 'set_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                values = []
                for val in args[4:]:
                    values.append(int(val))
                slave = server.get_slave(slave_id)
                slave.set_values(name, address, values)
                values = slave.get_values(name, address, len(values))
                sys.stdout.write('done: values written: %s\r\n' % (str(values)))

            elif args[0] == 'get_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                slave = server.get_slave(slave_id)
                values = slave.get_values(name, address, length)
                sys.stdout.write('done: values read: %s\r\n' % (str(values)))

            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
    finally:
        server.stop()
    
