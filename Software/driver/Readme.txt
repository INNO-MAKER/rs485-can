How to use 485&CAN module in a new Raspbian System


(1) Insert a TF cart into your computer, load your image of Raspbian to it

(2) Download the file named 'rs485_at.dtbo' from our wiki and copy it to /boot/overlays of the TF
card.

(3) Open config.txt and add below two lines in the end.
dtoverlay=rs485_at
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=25

(4) Insert the TF card into the Raspberry Pi and power on.

(5) Download test codes and copy the folder to the Raspberry Pi by USB flash Dsik or remote
login.

(6) Go into the folders and change the permission. Otherwise you can't run the Demo.
chmod -R a+x *

(7) Check the kernel log to see if RS485 was initialized successfully.
ls -l /dev/ttyS*

(8) Check the kernel log to see if CAN was initialized successfully.


If you want to use Python 
(1)Check the Python version of your Raspbian. Python 3.7.3 default in 2019-07-10-Raspbian.img.
Our Demo can

(2)If you can not find the Python3 in system. Install the Python3
sudo apt-get install python-pip
sudo apt-get install python3 idle3 nano

(3)Install Python CAN library.
sudo pip install python-can