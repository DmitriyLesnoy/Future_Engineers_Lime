import simulatorAPI as uapi
import cv2
import numpy as np
import time

robot = uapi.UnityAPI().make_car_robot("Robot")

manual_angle = 0
manual_throttle = 0

e_old = 0
timer_move = 0

# текущая стадия программы
state = 0
# название стадий
state_names = ["Manual move", "Auto movement"]

while True:
    frame = robot.camera.frame()
    k = cv2.waitKey(5)

    # если нажата клавиша 1
    if k == 49:
        # переключаем програму в 1 стадию
        state = 0
    # если нажата клавиша 2
    elif k == 50:
        # переключаем програму во 2 стадию
        state = 1

    if state == 0:
        # ручное управление

        if k == 119 or k == 246:
            manual_throttle += 5
            if manual_throttle>100:manual_throttle=100
        elif k == 115 or k == 251:
            manual_throttle -= 5
            if manual_throttle<-100:manual_throttle=-100
        elif k == 97 or k == 244:
            manual_angle -= 5
            if manual_angle < -35: manual_angle = -35
        elif k == 100 or k == 226:
            manual_angle += 5
            if manual_angle>35: manual_angle=35
        elif k == 32:
            # если нажата клавища пробел, сбрасываем угол и газ
            manual_angle = 0
            manual_throttle=0
            robot.brake(100,100)


        # отправляем команды на робота
        robot.move(manual_throttle)
        robot.turn(manual_angle)
        # телеметрия ручного управления
        cv2.putText(frame, "throttle: " + str(round(manual_throttle, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame, "angle: " + str(round(manual_angle, 1)), (10, 80),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

    if state == 1:
        # Автономное движение

        # например просто ехать вперед по кругу
        robot.move(50)
        robot.turn(35)








    # вывод телеметрии на экран
    cv2.putText(frame, "State: " + state_names[state], (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)
    cv2.putText(frame, "Speed: " + str(round(robot.sensor.get_speed(), 1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
