# rs485-and-can
## Quick Start
#### Step1,Download Software
`sudo git clone https://github.com/INNO-MAKER/rs485-can.git` </br>
`cd rs485-can`      
`chmod -R a+rwx *`
#### Step2,Install dtbo file
`uname -a`  #check your kernel version </br>
`sudo cp driver/rs485_at-kernel5.dtbo /boot/overlays/rs485_at.dtbo`      # For linux kernel version above 5.4

Note:</br> If your kernel is Linux 4.9,you need to use below command instead
`sudo cp driver/rs485_at-kernel4.dtbo /boot/overlays/rs485_at.dtbo`      
#### Step3,Revised config.txt
`sudo nano /boot/config.txt` #Add below two content to the last line
`dtoverlay=rs485_at`
`dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=25`
#Press ctrl+o save file,ctrl+x to exit editing.</br>
`sudo reboot`
