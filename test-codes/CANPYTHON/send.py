#################################################################################################

## Description :  This codes is for test the CAN function of 485&CAN module commuincation
##                on two Raspberry Pi.One run 'send.py', the other run 'receive.py'        
##                Sender send "0,1,2,3,4,5,6" to receiver

## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.08.22

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                SYstem of RPI       ----------------------  2019-07-10-raspbian-buster-full.img
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)

##################################################################################################


import os
import can

#check system name, in linux will print 'posix' and in windows will print 'nt'
print(os.name)


os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')

can1 = can.interface.Bus(channel = 'can1', bustype = 'socketcan_ctypes')

msg = can.Message(arbitration_id=0x123, data=[0,1,2,3,4,5,6], extended_id=False)
can1.send(msg)

os.system('sudo ifconfig can1 down')

