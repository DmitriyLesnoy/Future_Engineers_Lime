import os
#sudo apt-get install python3-pip
#sudo apt-get install python3-dev
#sudo pip3 install --no-use-wheel pyzmq
#sudo apt-get install openjdk-8-jdk automake autoconf
#sudo apt-get install curl zip unzip libtool swig libpng-dev zlib1g-dev pkg-config git g++ wget xz-utils
#sudo apt-get install python3-numpy python3-dev python3-pip python3-mock
# sudo apt-get install libjpeg-dev zlib1g-dev

#TPU Coral
#sudo apt-get install python3-edgetpu
# sudo pip3 install pyserial

#sudo apt-get install libgnutls28-dev

# sudo apt install libhdf5-100 -y
# sudo apt install libharfbuzz0b -y
# sudo apt install libwebp6 -y
# sudo apt install libjasper1 -y
# sudo apt install libilmbase12 -y
# sudo apt install libopenexr22 -y
# sudo apt install libgstreamer1.0-0 -y
# sudo apt install libavcodec-extra57 -y
# sudo apt install libavformat57 -y
# sudo apt install libswscale4 -y
# sudo apt install libgtk-3-0 -y
# sudo apt install libqtgui4 -y
# sudo apt install libqt4-test -y

#sudo apt-get install libatlas-base-dev -y
#sudo apt install python3-opencv
#sudo pip3 install opencv-python
#sudo pip3 install opencv-contrib-python
#sudo pip3 install tensorflow
# для 4 rasp
#sudo apt install python3-opencv

# print(os.system('sudo pip3 install --upgrade pip'))
# print(os.system('sudo pip3 install keras==2.1.5'))
# print(os.system('sudo apt-get install libgstreamer-plugins-base0.10-0 -y'))


#для стерео камеры
# print(os.system('sudo apt-get install gstreamer-1.0 -y'))
# print(os.system('sudo apt-get install libqtgui4 -y'))
# print(os.system('sudo apt install libqt4-test -y'))
#print(os.system('sudo pip3 install opencv-contrib-python'))
#print(os.system('sudo systemctl disable autostart.service'))
#
#
#os.system('sudo python3 /home/pi/robot/set_password.py 111111')
#os.system('sudo pip3 install pyserial')
# os.system('sudo pip3 install crccheck')
#os.system('sudo pip3 install opencv-contrib-python')
#os.system('sudo pip3 install flask')
print(os.system('ifconfig'))
import time
time.sleep(5)

# os.system('sudo cp /home/pi/robot/dhcpcd.conf.point /etc/dhcpcd.conf')
# os.system('sudo cp /home/pi/robot/dhcpcd.conf.route /etc/dhcpcd.conf')
os.system('sudo shutdown -r now')
os.system('ls')