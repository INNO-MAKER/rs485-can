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
import serial
import fcntl
import os
import struct
import termios
import array
#import modbus lib
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
#import modbus_tk.modbus_rtu as modbus_rtu
from modbus_tk import modbus_rtu

# RS485 ioctls define
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
#end of rs485_enable():

       
if __name__ == '__main__':
    
    logger = modbus_tk.utils.create_logger("console")

    rs485_enable()

    #set modbus master
    master = modbus_rtu.RtuMaster(
           serial.Serial(port= '/dev/ttySC0',
           baudrate=9600,
           bytesize=8,
           parity='N',
           stopbits=1,
           xonxoff=0)
       )
    
    master.set_timeout(5.0)
    master.set_verbose(True)
    logger.info("connected")
    
    logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))
    
    #send some queries
    #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
    #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
    #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
    #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
    #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
    #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
    #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
    #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))
    
#end of if __name__ == '__main__':     
    