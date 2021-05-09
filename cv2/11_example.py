import RobotAPI as rapi
import cv2
import numpy as np

robot = rapi.RobotAPI(flag_pyboard=1)

low = np.array([0, 0, 0])
up = np.array([255, 255, 80])

Y1, Y2, X1, X2 = 380, 480, 0, 310
p = 0
while 1:
    while robot.button() == 0:
        pass
    while robot.button() == 0:

        frame = robot.get_frame(wait_new_frame=1)
        frame_small = frame[Y1: Y2, X1:X2].copy()

        hsv = cv2.cvtColor(frame_small, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low, up)
        gray_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        flag_p = False
        for contur in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > 500:
                e = 80 - (x + w / 2)
                print(e)
                p = e * 0.2
                robot.serv(p)
                robot.move(255, 0, 50)

                cv2.drawContours(frame_small, contour, -1, (0, 0, 255), 3)
        if flag_p == False:
            robot.move(200, 0, 50)
            if p >= 0:
                robot.serv(35)
            elif p <= 0:
                robot.serv(-35)

        frame1 = np.vstack([frame_small, gray_image])
        # frame = np.vstack([frame, frame1])

        robot.set_frame(frame1)
