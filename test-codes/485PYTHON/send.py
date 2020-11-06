#################################################################################################

## Description :  This codes is for test the 485 function of 485&CAN module commuincation
##                on two Raspberry Pi.One run 'send.py', the other run 'receive.py'      
##                Sender send "a,b,c,d" to receiver

## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.08.22

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                SYstem of RPI       ----------------------  2019-07-10-raspbian-buster-full.img
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

##################################################################################################


import serial
import fcntl
import os
import struct
import termios
import array
import time

# RS485 ioctls
TIOCGRS485 = 0x542E
TIOCSRS485 = 0x542F
SER_RS485_ENABLED = 0b00000001
SER_RS485_RTS_ON_SEND = 0b00000010
SER_RS485_RTS_AFTER_SEND = 0b00000100
SER_RS485_RX_DURING_TX = 0b00010000


buf = array.array('i', [0] * 8) # flags, delaytx, delayrx, padding
ser = serial.Serial("/dev/ttySC0",115200)
fcntl.ioctl(ser, TIOCGRS485, buf)

buf[0] |=  SER_RS485_ENABLED|SER_RS485_RTS_AFTER_SEND
buf[1]  = 0
buf[2]  = 0
fcntl.ioctl(ser, TIOCSRS485, buf)



print (ser.portstr)
command = ['a','b','c','d']
#strInput = raw_input('enter some words:')    
#while True:
n = ser.write(command)    
    #print (n)    
    #str = t.read(n)    
    #print (str)   

