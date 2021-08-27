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



# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial



ser = serial.Serial("/dev/ttySC1",115200)

print (ser.portstr) 
while True:  
    #str = ser.readall()  
    str = ser.read(ser.inWaiting())
    #print (str)
    if str:
        print ("Recv some data : ")
        print (str)


