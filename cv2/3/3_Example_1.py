import simulatorAPI as uapi
import cv2
import numpy as np
import time

robot = uapi.UnityAPI().make_cv_robot("Robot")

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

manual_angle = 0
manual_throttle = 100
flag_drill = False
e_old = 0

while True:
    frame = robot.camera.frame()
    cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)
    cv2.aruco.drawDetectedMarkers(frame, cords, ids)

    if ids is not None:
        for i, aruco_code in enumerate(ids):
            aruco_code = int(aruco_code)

            x, y, w, h = cv2.boundingRect(cords[i][0])
            print("finded code:", aruco_code, (x, y, w, h))

    k = cv2.waitKey(10)
    if k != -1:
        print(k)
    # ручное управление
    if k == 13:
        flag_drill = not flag_drill
        robot.drill.power("on") if flag_drill else robot.drill.power("off")
        print("Flag Drill", flag_drill)
    elif k == 8:
        # при нажатии backspaсe выбрасываем ресурсы
        robot.connector1.drop_all()
        print("Drop all from container")
    elif k == 113:
        manual_angle -= 1
        robot.rotor0.angle(manual_angle)
    elif k == 101:
        manual_angle += 1
        robot.rotor0.angle(manual_angle)
    elif k == 119 or k == 246:
        robot.move(manual_throttle, manual_throttle)
    elif k == 115 or k == 251:
        robot.move(-manual_throttle, -manual_throttle)
    elif k == 97 or k == 244:
        robot.move(-manual_throttle, manual_throttle)
    elif k == 100 or k == 226:
        robot.move(manual_throttle, -manual_throttle)
    elif k == 32:
        manual_angle = 0
        robot.rotor0.angle(manual_angle)
        robot.brake(-100, -100)

    # вывод телеметрии на экран
    cv2.putText(frame, "Cargo: " + str(len(robot.container.items())) + " item", (10, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.putText(frame, "Speed: " + str(round(robot.sensor.get_speed(), 1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.imshow("Frame", frame)
