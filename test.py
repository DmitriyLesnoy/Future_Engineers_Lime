import RobotAPI as rapi
import time
import cv2
import numpy as np
import regulators


robot = rapi.RobotAPI(flag_pyboard=True)

reg_move = regulators.Regulators(0, 0, 0, Ki_border=5)

manual_angle = 0
manual_throttle = 0

e_old = 0


# текущая стадия программы
state = 1
# название стадий
state_names = ["Manual move", "Auto movement", "Left", "Forward", "Right"]

# фильтр черного цвета

low_b = np.array([0, 0, 0])
up_b = np.array([255, 255, 50])

low_orange = np.array([0, 50, 80])
up_orange = np.array([50, 255, 120])

low_blue = np.array([85, 170, 70])
up_blue = np.array([125, 255, 225])

timer_stop = 0
i = 0
start_flag = True

flag_move=1

count_turn=0
finish_circles=3

global_speed=60

while 1:
    frame = robot.get_frame(wait_new_frame=1)

    k = robot.get_key()
    print(k)
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
        timer_move = time.tine()


    if state == 2:
        pass
    if state == 3:
        pass
    if state == 4:
        pass
    if state == 0:
        # ручное управление

        if k == 37:
            manual_serv = 35
            robot.serv(manual_serv)
            # print(manual_serv)
        if k == 39:
            manual_serv = -35
            robot.serv(manual_serv)
            # print(manual_serv)
        if k == 32:
            manual_serv = 0
            robot.serv(manual_serv)
            # print(manual_serv)
        if k == 87:
            robot.move(10, 0, 50, wait=False)
        if k == 83:
            robot.move(-10, 0, -50, wait=False)


        # отправляем команды на робота
        # robot.move(manual_throttle)
        # robot.serv(manual_angle)
        # телеметрия ручного управления
        cv2.putText(frame, "throttle: " + str(round(manual_throttle, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame, "angle: " + str(round(manual_angle, 1)), (10, 80),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

    if state == 2:
        # ПОВОРОТ ВПРАВО

        # robot.lamp.rgb(0, 0, 1)
        cv2.putText(frame, "timer: " + str(round(time.time() - timer_stop, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

        # едем прямо 2 секунды, а потом переключаемся в 1 стадию
        if time.time() < timer_stop + 2:
            if flag_move:
                robot.move(global_speed,0, 100, wait=0)
                robot.serv(-35)

        if time.time() > timer_stop + 0.9:
            state = 1
            count_turn += 1
            #print(count_turn)
        if (finish_circles*4)==count_turn:
            flag_move=False
    if state == 3:
        #ПОВОРОТ ВЛЕВО

        cv2.putText(frame, "timer: " + str(round(time.time() - timer_stop, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

        # едем прямо 2 секунды, а потом переключаемся в 1 стадию
        if time.time() < timer_stop + 2:
            if flag_move:
                robot.move(global_speed, 0, 100, wait=0)
                robot.serv(35)

        if time.time() > timer_stop + 0.9:
            state = 1
            count_turn += 1
            # print(count_turn)
        if (finish_circles * 4) == count_turn:
            flag_move = False

    if state == 1:

        # x1, y1 = 0, 0
        # x2, y2 = 20, 249*2
        # # вырезаем часть изображение
        # frame_crop = frame[y1:y2, x1:x2]
        # # cv2.imshow("frame_crop", frame_crop)
        # # рисуем прямоугольник на изображении
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # # переводим изображение с камеры в формат HSV
        # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
        # # фильтруем по заданным параметрам
        # mask = cv2.inRange(hsv, low_b, up_b)
        # # выводим маску для проверки
        # # cv2.imshow("mask", mask)
        # # на отфильтрованной маске выделяем контуры
        # im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #
        # max_c=0
        # for contour in contours:
        #     # Создаем прямоугольник вокруг контура
        #     x, y, w, h = cv2.boundingRect(contour)
        #     # вычисляем площадь найденного контура
        #     area = cv2.contourArea(contour)
        #     if area > 50:
        #         if max_c< y+h:
        #             max_c = y+h
        #         # отрисовываем найденный контур
        #         cv2.drawContours(frame_crop, contour, -1, (0, 0, 255), 2)
        #
        # if max_c>0:
        #     porog=280
        #
        #     reg_move.set(0.8, 0, 0.03)
        #
        #     p = reg_move.apply(porog, max_c)   #min_x_r
        #
        #     # e = 240 - max_c
        #     # p = e * 0.8
        #
        #     robot.serv(p)
        #     # print(max_c, -p)
        #     # if start_flag:
        #     #     print(e)
        #     #     start_flag = False
        robot.serv(5)
        robot.move(10,0,50,wait=0)

        x1, y1 = 320 - 10*2, 200*2-100
        x2, y2 = 320 + 10*2, 230*2-100
        # вырезаем часть изображение
        frame_crop = frame[y1:y2, x1:x2]
        # cv2.imshow("frame_crop", frame_crop)
        # рисуем прямоугольник на изображении
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # переводим изображение с камеры в формат HSV
        hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
        # фильтруем по заданным параметрам
        mask = cv2.inRange(hsv, low_blue, up_blue)
        # выводим маску для проверки
        # cv2.imshow("mask", mask)
        # на отфильтрованной маске выделяем контуры
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # перебираем все найденные контуры
        flag_line = False
        for contour in contours:
            # Создаем прямоугольник вокруг контура
            x, y, w, h = cv2.boundingRect(contour)
            # вычисляем площадь найденного контура
            area = cv2.contourArea(contour)
            if area > 50:
                # отрисовываем найденный контур
                # cv2.drawContours(frame_crop, contour, -1, (0, 0, 255), 2)
                # включаем зеленый свет
                # robot.lamp.rgb(0, 1, 0)
                # robot.turn(p)
                # # даем газу,если скорость низкая
                # if robot.sensor.get_speed() < 7:
                #     robot.move(30)
                #     pass
                i += 1
                robot.beep()
                timer_stop = time.time()

        if flag_move:
            robot.move(global_speed,0,40,wait=0)

        # robot.serv(0)
        # if i > 4:
        #     break

    # вывод телеметрии на экран
    cv2.putText(frame, "State: " + state_names[state], (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)
    # cv2.putText(frame, "Speed: " + str(round(robot.sensor.get_speed(), 1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
    #             (0, 0, 255), 2)

    # cv2.imshow("Frame", frame)
    robot.set_frame(frame)

# robot.brake(100, 10000)
# time.sleep(1)
