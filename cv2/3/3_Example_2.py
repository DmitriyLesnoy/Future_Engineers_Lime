import simulatorAPI as uapi
import cv2
import numpy as np
import time

robot = uapi.UnityAPI().make_cv_robot("Robot")

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

manual_angle = 0
manual_throttle = 100
flag_drill = False
e_old=0

# текущая стадия программы
state = 1

while True:
    frame = robot.camera.frame()
    k = cv2.waitKey(10)

    # если нажата клавиша 1
    if k ==49:
        # переключаем програму в 1 стадию
        state = 1
    # если нажата клавиша 2
    elif k==50:
        # переключаем програму во 2 стадию
        state = 2
    # если нажата клавиша 3
    elif k==51:
        # переключаем програму в 3 стадию
        state = 3


    if state == 1:
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
            # сброс ресурсов из контейнера
            robot.connector1.power("on")
            robot.connector1.drop_all()
            print("Drop all")

    if state==2:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)

        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==47:
                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if state==3:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)


        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==48:
                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


    # вывод телеметрии на экран
    cv2.putText(frame, "Cargo: "+ str(len(robot.container.items()))+ " item", (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.putText(frame, "Speed: "+ str(round(robot.sensor.get_speed(),1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.putText(frame, "State: "+ str(state), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.imshow("Frame", frame)

