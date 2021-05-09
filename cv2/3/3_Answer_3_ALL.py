import simulatorAPI as uapi
import cv2
import numpy as np
import time

robot = uapi.UnityAPI().make_cv_robot("Robot")
robot.drill.power()

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

manual_angle = 0
manual_throttle = 100
flag_drill = False
e_old=0

# текущая стадия программы
state = 7

time_move = 0

while True:
    frame = robot.camera.frame(wait_new_frame=True)
    k = cv2.waitKey(1)
    if k!=-1:
        print(k)
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
    elif k==52: state = 4
    elif k==53: state = 5
    elif k==54: state = 6
    elif k==55: state = 7
    elif k==56: state = 8


    if state == 1:
        # ручное управление
        if k == 13:
            flag_drill = not flag_drill
            robot.drill.power("on") if flag_drill else robot.drill.power("off")
            print("Flag Drill", flag_drill)

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

        flag_move = False
        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==47:
                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        if w>90:
                            state = 3

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        e = 320 // 2 - (x + w / 2)
                        p = e * 0.2 - (e_old - e) * 0.5
                        e_old = e

                        speed = 20
                        if robot.sensor.get_speed()>3:
                            speed=0
                        robot.move(speed - p, speed + p)
                        flag_move = True
                        time_move = time.time()
                        break
        if flag_move==False and  time.time()>time_move+1:
            robot.move(-30,30)
    if state==3:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)
        flag_move = False
        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==48:

                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        if w>90:
                            state = 4

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        e = 320 // 2 - (x + w / 2)
                        p = e * 0.1 - (e_old - e) * 0.5
                        e_old = e

                        speed = 30
                        if robot.sensor.get_speed()>5:
                            speed=0

                        robot.move(speed - p, speed + p)
                        flag_move = True
                        time_move = time.time()
                        break
        if flag_move==False and  time.time()>time_move+1:
            robot.move(-30,30)
    if state==4:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)
        flag_move = False
        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==0:

                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        if w>90:
                            state = 5
                            robot.connector1.drop_all()


                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        e = 320 // 2 - (x + w / 2)
                        p = e * 0.1 - (e_old - e) * 0.5
                        e_old = e

                        speed = 30
                        if robot.sensor.get_speed()>5:
                            speed=0

                        robot.move(speed - p, speed + p, wait=False)
                        flag_move = True
                        time_move = time.time()
                        break
        if flag_move==False and  time.time()>time_move+1:
            robot.move(-30,30)
    if state==5:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)
        flag_move = False
        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==48:

                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        if w>90:
                            state = 6
                            robot.drill.power()

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        e = 320 // 2 - (x + w / 2)
                        p = e * 0.1 - (e_old - e) * 0.5
                        e_old = e

                        speed = 60
                        if robot.sensor.get_speed()>3:
                            speed=1

                        robot.move(speed - p, speed + p)
                        flag_move = True
                        time_move = time.time()
                        break
        if flag_move==False and  time.time()>time_move+1:
            robot.move(-30,30)
    if state==6:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)
        flag_move = False
        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==47:

                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        if w>90:
                            state = 7
                            robot.drill.power()


                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        e = 320 // 2 - (x + w / 2)
                        p = e * 0.2 - (e_old - e) * 0.5
                        e_old = e

                        speed = 30
                        if robot.sensor.get_speed()>5:
                            speed=0

                        robot.move(speed - p, speed + p)
                        flag_move = True
                        time_move = time.time()
                        break
        if flag_move==False and  time.time()>time_move+1:
            robot.move(-30,30)
    if state==7:

        if len(robot.container.items())>3:
            state = 8


        low = np.array([93, 104, 0])
        up = np.array([107, 256, 256])
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low, up)
        gray_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        max_area = 0;
        max_contour = ()
        flag_move = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        if max_area > 0:
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.drawContours(frame, max_contour, -1, (0, 0, 255), 2)
            robot.lamp.rgb(0, 1, 0)

            e = 320 // 2 - (x + w / 2)
            p = e * 0.1 - (e_old - e) * 0.9
            e_old = e
            # print(p)
            # print(robot.sensor.get_speed())
            speed = 0
            if robot.sensor.get_speed() < 10:
                speed = 30

            robot.move(speed - p, speed + p)
            flag_move = True
            time_move = time.time()
            time_last_detect_target = time.time()

        if flag_move==False and  time.time()>time_move+1:
            robot.lamp.rgb(1, 0, 0)
            robot.move(-30, 30)
            print("protect")

    if state==8:
        # движение к аруке
        cords, ids, rest = cv2.aruco.detectMarkers(frame, dictionary)
        flag_move = False
        if ids is not None:
                for i, aruco_code in enumerate(ids):
                    aruco_code = int(aruco_code)
                    if aruco_code==47:
                        state = 2
                    if aruco_code==1:

                        x, y, w, h = cv2.boundingRect(cords[i][0])
                        if w>130:
                            state = 2
                            # robot.connector1.drop_all()

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        e = 320 // 2 - (x + w / 2)
                        p = e * 0.2 - (e_old - e) * 0.3
                        e_old = e

                        speed = 30
                        if robot.sensor.get_speed()>10:
                            speed=0

                        robot.move(speed - p, speed + p)
                        flag_move = True
                        time_move = time.time()
                        break
        if flag_move==False and time.time()>time_move+1:
            robot.move(-30,30)

    # вывод телеметрии на экран
    cv2.putText(frame, "Cargo: "+ str(len(robot.container.items()))+ " item", (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.putText(frame, "Speed: "+ str(round(robot.sensor.get_speed(),1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.putText(frame, "State: "+ str(state), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.imshow("Frame", frame)

