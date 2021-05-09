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
state = 1
# название стадий
state_names = ["Manual move", "Auto movement", "Left", "Forward", "Right"]

# фильтр черного цвета

low = np.array([0, 0, 00])
up = np.array([ 180, 80, 115])

timer_stop = 0

while True:
    frame = robot.camera.frame()

    k = cv2.waitKey(1)

    # если нажата клавиша 1
    if k == 49:
        # переключаем програму в 1 стадию
        state = 0
    # если нажата клавиша 2
    elif k == 50:
        # переключаем програму во 2 стадию
        state = 1
    elif k == 51:
        # переключаем програму в 3 стадию
        state = 2
        timer_stop = time.time()

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

    if state == 2:
        robot.lamp.rgb(0, 0, 1)
        cv2.putText(frame, "timer: " + str(round(time.time()-timer_stop, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)


        # едем прямо 2 секунды, а потом переключаемся в 1 стадию
        if time.time() < timer_stop + 4:
            robot.move(50)
            robot.turn(0)

        if time.time() > timer_stop + 4:
            state = 1


    if state == 1:


        # Автономное движение по линии


        x1, y1 = 120, 150
        x2, y2 = 320, 170
        # вырезаем часть изображение
        frame_crop = frame[y1:y2, x1:x2]
        # cv2.imshow("frame_crop", frame_crop)
        # рисуем прямоугольник на изображении
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # переводим изображение с камеры в формат HSV
        hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
        # фильтруем по заданным параметрам
        mask = cv2.inRange(hsv, low, up)
        # выводим маску для проверки
        # cv2.imshow("mask", mask)
        # на отфильтрованной маске выделяем контуры
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # перебираем все найденные контуры
        flag_line = False
        for contour in contours:
            # Создаем прямоугольник вокруг контура
            x, y, w, h = cv2.boundingRect(contour)
            # вычисляем площадь найденного контура
            area = cv2.contourArea(contour)
            if area > 5:
                flag_line=True
                # отрисовываем найденный контур
                cv2.drawContours(frame_crop, contour, -1, (0, 0, 255), 2)
                # включаем зеленый свет
                robot.lamp.rgb(0, 1, 0)
                target = 100
                cv2.circle(frame, (int(x1 + target), y1), 10, (0, 255, 0), 2)
                line_x = x
                # print(line_x)
                cv2.circle(frame, (int(x1+line_x), y1), 10, (255, 0, 0), 2)
                e  = line_x - target
                p = e*0.3
                robot.turn(p)
                # даем газу,если скорость низкая
                if robot.sensor.get_speed()<7:
                    robot.move(30)
                    pass

        if flag_line==False:
            #слет с линии
            print("No line")

    # вывод телеметрии на экран
    cv2.putText(frame, "State: " + state_names[state], (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)
    cv2.putText(frame, "Speed: " + str(round(robot.sensor.get_speed(), 1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
