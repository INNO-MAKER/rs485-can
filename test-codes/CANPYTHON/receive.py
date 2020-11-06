#################################################################################################

## Description :  This codes is for test the CAN function of 485&CAN module commuincation
##                on two Raspberry Pi.One run 'send.py', the other run 'receive.py'      
##                Sender send "0,1,2,3" to receiver

## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.08.22

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                SYstem of RPI       ----------------------  2019-07-10-raspbian-buster-full.img
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

##################################################################################################


import os
import can

os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

while True:
    msg = can0.recv(30.0)
    print (msg)
    if msg is None:
        print('No message was received')
    
       
os.system('sudo ifconfig can0 down')
