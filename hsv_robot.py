import RobotAPI as rapi

robot = rapi.RobotAPI(flag_serial=False)

import cv2
import numpy as np
import time

HUE_MIN = 0
HUE_MAX = 256
SAT_MIN = 0
SAT_MAX = 256
VAL_MIN = 0
VAL_MAX = 256
# low_g = np.array([40, 195, 80])
# up_g = np.array([80, 256, 140])
HUE_MIN = 0
HUE_MAX = 256
SAT_MIN = 0
SAT_MAX = 256
VAL_MIN = 0
VAL_MAX = 80

trackbar_vals = {'min': np.array([HUE_MIN, SAT_MIN, VAL_MIN]),
                 'max': np.array([HUE_MAX, SAT_MAX, VAL_MAX])}

show_frame = 1
frame = robot.get_frame()
timer_print=time.time()
while True:
    if show_frame:
        frame = robot.get_frame()
    m = robot.get_key()
    if m != -1:
        # print(m)
        if m == 8 or m == 13:
            if show_frame == 0:
                show_frame = 1
            else:
                show_frame = 0
        if m == 32:
            HUE_MIN = 0
            HUE_MAX = 256
            SAT_MIN = 0
            SAT_MAX = 256
            VAL_MIN = 0
            VAL_MAX = 256
        step = 5
        if m == 81:
            trackbar_vals['min'][0] -= step
        if m == 87:
            trackbar_vals['min'][0] += step

        if m == 69:
            trackbar_vals['max'][0] -= step
        if m == 82:
            trackbar_vals['max'][0] += step

        if m == 65:
            trackbar_vals['min'][1] -= step
        if m == 83:
            trackbar_vals['min'][1] += step

        if m == 68:
            trackbar_vals['max'][1] -= step
        if m == 70:
            trackbar_vals['max'][1] += step

        if m == 90:
            trackbar_vals['min'][2] -= step
        if m == 88:
            trackbar_vals['min'][2] += step

        if m == 67:
            trackbar_vals['max'][2] -= step
        if m == 86:
            trackbar_vals['max'][2] += step
        if m == 32:
            trackbar_vals['max'][:] = 255
            trackbar_vals['min'][:] = 0

        for i in range(3):
            trackbar_vals['max'][i] = robot.constrain(trackbar_vals['max'][i], 0, 255)
            trackbar_vals['min'][i] = robot.constrain(trackbar_vals['min'][i], 0, 255)

    # ret, frame = cap.read()

    imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imageHSV, trackbar_vals['min'], trackbar_vals['max'])
    if timer_print<time.time():
        print(trackbar_vals['min'], trackbar_vals['max'])
        timer_print = time.time()+0.5
    frame_hsv = cv2.bitwise_or(frame, frame, mask=mask)
    # cv2.imshow("Video image", cv2.bitwise_or(frame, frame, mask=mask))
    # if cv2.waitKey(30) == 32:
    #     break
    robot.set_frame(frame_hsv)
