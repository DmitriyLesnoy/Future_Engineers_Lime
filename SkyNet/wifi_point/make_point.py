#sudo apt update
#sudo apt full-upgrade


import os
# import io
#
#
# with io.open("/etc/hostapd/hostapd.conf", mode='w', encoding='utf-8') as text_file:
#     # f.write(my_string)
# # text_file = open("/etc/hostapd/hostapd.conf", "w")
#     text_file.write('interface=wlan0\n')
#     text_file.write('driver=nl80211\n')
#     text_file.write('ssid=Rasp\n')
#     text_file.write('hw_mode=g\n')
#     text_file.write('channel=7\n')
#     text_file.write('wmm_enabled=0\n')
#     text_file.write('macaddr_acl=0\n')
#     text_file.write('auth_algs=1\n')
#     text_file.write('ignore_broadcast_ssid=0\n')
#     text_file.write('wpa=2\n')
#     text_file.write('wpa_passphrase=321321321\n')
#     text_file.write('wpa_key_mgmt=WPA - PSK\n')
#     text_file.write('wpa_pairwise=TKIP\n')
#     text_file.write('rsn_pairwise=CCMP\n')
# text_file.close()

# with open("/etc/hostapd/hostapd.conf", "w") as text_file:
#     text_file.writelines('interface=wlan0\n')
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
#     text_file.writelines()
# text_file.close()

#make point

MAKE_POINT=1

if MAKE_POINT:
    os.system('sudo cp /home/pi/robot/hostapd.conf /etc/hostapd/hostapd.conf')
    os.system('sudo cp /home/pi/robot/dhcpcd.conf.point /etc/dhcpcd.conf')

else:
    #make route connect to SkyNet
    os.system('sudo cp /home/pi/robot/dhcpcd.conf.route /etc/dhcpcd.conf')

os.system('sudo shutdown -r now')

