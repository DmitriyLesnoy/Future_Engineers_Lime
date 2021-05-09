import simulatorAPI as uapi
import time
import cv2

robot = uapi.UnityAPI().make_cv_robot("Robot")

manual_throttle = 50

robot.lamp.rgb(0, 0, 1)
# robot.move(50,-50, 800)
# time.sleep(2)
robot.move(100,100, 6000)
time.sleep(6)


#
# robot.move(50,50, 1000)
# time.sleep(1)
# robot.move(50,50, 1000)
# time.sleep(1)

while True:
    frame = robot.camera.frame()

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)

    if k!=-1:
        print(k)


    if k == 119 or k == 246:
        robot.move(-50,-50)
        robot.lamp.rgb(0, 0, 1)
    elif k ==97:
        robot.move(-50, 50)
    elif k == 32:
        robot.lamp.rgb(1, 1, 1)
        print(robot.sensor.get_position())

