#################################################################################################

## Description :  This codes is use for production test for 485&CAN module.
##                Two groups 485 direct docking, and CAN Port connect to USB&CAN for test
##                CAN function

## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.08.22

## Environment :  Hardware            ----------------------  Raspberry Pi 4 + 485&CAN+ USB2CAN
##                SYstem of RPI       ----------------------  2019-07-10-raspbian-buster-full.img
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

##################################################################################################



import serial
import fcntl
import os
import struct
import termios
import array
import can


# RS485 ioctls
TIOCGRS485 = 0x542E
TIOCSRS485 = 0x542F
SER_RS485_ENABLED = 0b00000001
SER_RS485_RTS_ON_SEND = 0b00000010
SER_RS485_RTS_AFTER_SEND = 0b00000100
SER_RS485_RX_DURING_TX = 0b00010000
# rs 485 port
ser1 = serial.Serial("/dev/ttySC0",115200)    
ser2 = serial.Serial("/dev/ttySC1",115200)

# CAN Port
#Set CAN0 speed to 1M bps
os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')
#Set CAN1 speed to 1M bps
os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')
can1 = can.interface.Bus(channel = 'can1', bustype = 'socketcan_ctypes')

#function
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

def rs485_test():
    rs485_enable()
    command = ['a','b','c','d','e','f','g']
    n = ser1.write(command)
    #str = ser2.read(ser2.inWaiting())
    str = ser2.read(7)
    if((str[0] == 'a')and(str[1] =='b')and(str[2] == 'c')and(str[3] == 'd')
       and(str[4] == 'e')and(str[5] == 'f')and(str[6] == 'g')):
       print("485 TEST SUCCESSFUL----------\r\n"*3)
    else:
       print("485 TEST Failure!!!!!!!!\r\n"*3)
    
def can_test():

    ##  CAN0 SEND AND CAN1 RECEIVE    
    msg = can.Message(arbitration_id=0x123, data=[0x55,0xaa,0x5a,0xa5],
                  extended_id=False)

    can0.send(msg)
    msg = can1.recv(10.0)

    if((msg.data[0] == 0x55)and(msg.data[1] == 0xaa)and
   (msg.data[2] == 0x5a)and(msg.data[3] == 0xa5)):
    ##  CAN1 SEND AND CAN0 RECEIVE     
        msg = can.Message(arbitration_id=0x123, data=[0x55,0xaa,0x5a,0xa5],
                      extended_id=False)
    #print(msg)
        can1.send(msg)
        msg = can0.recv(30.0)
        if((msg.data[0] == 0x55)and(msg.data[1] == 0xaa)
           and(msg.data[2] == 0x5a)and(msg.data[3] == 0xa5)):
            #print(msg)
            print('CAN  TEST SUCCESSFUL----------\r\n'*3)

        elif msg is None:    ## No data
            print('Timeout CAN test failure!!!!\r\n'*3)
        else :
            print('Data1 validation errors!!!\r\n'*3)
            print(msg)                       ##print the err data
    
    elif msg is None: ## No data
        print('Timeout CAN test failure!!!\r\n'*3)
    else :     ##print the err data
        print('Data2 validation errors!!!\r\n'*3)
        print(msg)      
    
    os.system('sudo ifconfig can1 down')
    os.system('sudo ifconfig can0 down')
         
if __name__ == '__main__':    
    rs485_test()
    can_test() 
