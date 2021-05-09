import simulatorAPI as uapi
import cv2
import time
import numpy as np

# подключиться и создать объект робот
robot = uapi.UnityAPI().make_drone_robot("Drone")
throttle = 100

import threading

class OpticFlow(object):
    # max_points = 500


    def __init__(self, camera,max_point=50, min_point =5, k=1):

        self.x_delta, self.y_delta = 0,0
        self.p1, self.p0 = [],[]
        self.min_point = min_point
        self.max_points = max_point
        self.camera = camera
        self.feature_params = dict(maxCorners=self.max_points, qualityLevel=0.003, minDistance=70, blockSize=70)
        self.lk_params = dict(winSize=(25, 25),maxLevel=2,criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.k = k
        self.old_frame = self.camera.frame()
        if k!=1:
            self.old_frame = cv2.resize(self.camera.frame(), None, fx=self.k, fy=self.k, interpolation=cv2.INTER_CUBIC)

        self.old_gray = cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)
        self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask=None, **self.feature_params)
    #     self.my_thread = threading.Thread(target=self.thread_work)
    #     self.my_thread.daemon = True
    #     self.my_thread.start()
    # def thread_work(self):
    #     while 1:
    #         self.work(1)ws
    def work(self, show = False):
        try:
            self.frame = self.camera.frame().copy()
            if self.k != 1:
                self.frame = cv2.resize(self.frame, None, fx=self.k, fy=self.k, interpolation=cv2.INTER_CUBIC)

            self.frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # self.frame_gray = cv2.resize(self.frame_gray, None, fx=self.k, fy=self.k)
            if len(self.p0) < self.min_point:
                self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask=None, **self.feature_params)

            self.p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, self.frame_gray, self.p0, None, **self.lk_params)

            good_new = self.p1[st == 1]
            good_old = self.p0[st == 1]

            self.old_gray = self.frame_gray
            self.p0 = good_new.reshape(-1, 1, 2)

            X , Y= np.array([]),np.array([])
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                X = np.append(X, (a - c))
                Y = np.append(Y, (b - d))
                self.x_delta = (np.median(X))
                self.y_delta = (np.median(Y))

                if show:
                    self.frame = cv2.circle(self.frame, (int(a), int(b)), 5, (0,255,0), -1)
                    cv2.imshow("frame flow", self.frame)
                    cv2.waitKey(1)


        except Exception as e:
            # print("flow error", e)
            self.__init__(self.camera)


op = OpticFlow(robot.camera)

while True:

    op.work(show=True)

    frame = robot.camera.frame()

    keys = robot.get_keys()
    if 81 in keys:
        robot.gyro.add_torque_y(-100)
    if 69 in keys:
        robot.gyro.add_torque_y(100)

    if 87 in keys:
        robot.DroneController.forward(100)

    if 83 in keys:
        robot.DroneController.back(100)

    if 68 in keys:
        robot.DroneController.right(100)

    if 65 in keys:
        robot.DroneController.left(100)

    if 67 in keys:
        robot.DroneController.down(100)

    if 32 in keys:
        robot.DroneController.up(100)

    print(op.x_delta, op.y_delta)
    cv2.putText(frame, "x delta: " + str(round(op.x_delta, 2)), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
    cv2.putText(frame, "y delta: " + str(round(op.y_delta, 2)), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
    cv2.putText(frame, "laser sensor: " + str(round(robot.laser_sensor.get_dist(), 2)), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
