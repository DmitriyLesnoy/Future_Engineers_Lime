import time
t = time.time()
import RobotAPI as rapi


robot = rapi.RobotAPI()

print("Start RAW, RobotAPI loaded", round(time.time()-t,2))

robot.manual_regim=1
# robot.beep()
#robot.red()
# robot.move(255,255,300)
#robot.set_camera_high_res()
import cv2
# import os
# os.system('ls /dev')


import time

print("cv2 version",cv2.__version__)
print("robot API version", rapi.__version__)
t=0
while 1:
    frame = robot.get_frame(wait_new_frame=1)
    # frame = robot.get_frame()
    # frame = cv2.resize(frame, (640//8,480//8))
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if time.time()-t>5:
        t=time.time()
        f = open("/sys/class/thermal/thermal_zone0/temp", "r")
        temp = int(f.readline())/1000
        print(temp)

    # time.sleep(0.1)
    if robot.manual() == 1:
         continue


    robot.set_frame(frame, 10)
    # robot.wait(100)
