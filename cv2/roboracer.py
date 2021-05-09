import RobotAPI as rapi
import time
import cv2
import numpy as np
import regulators

robot = rapi.RobotAPI(flag_pyboard=True)

print("Start Roboracers")

flag_move = 0
flag_show = 0

speed = 190  # 140 190

faza = 1

fps_timer = time.time()
fps_count = 0
fps = 0
robot.manual_regim = 0

p = 0
timer_get_key = 0
manual_serv = 0
frame_show = robot.get_frame().copy()
reg_move = regulators.Regulators(0, 0, 0, Ki_border=5)

robot.set_camera(100, 640, 480)

low = np.array([0, 0, 0])
up = np.array([256, 256, 80])
robot.button()

while True:
    # print(robot.vcc())
    #
    # if robot.button() == 1:
    #     print("Push")
    #     flag_move = True

    if time.time() > timer_get_key or faza == 0:
        timer_get_key = time.time() + 0.05
        m = robot.get_key()
    else:
        m = -1
    if m != -1:
        # print(m)
        pass

    if m == 49:
        faza = 0
        print("faza 0 manual mode")
    if m == 50:
        faza = 1
        print("faza 1 move line cv")
    if m == 51:
        faza = 3
        print("faza 3 mask")

    if m == ord('T'):
        robot.tone(420, 50)
        robot.tone(1020, 50)
        robot.tone(2020, 110)

    if m == ord('O'):
        robot.odometr_reset()

    if m == ord('M'):
        flag_move = not flag_move
        print("change flag move", flag_move)
        time.sleep(0.1)
        robot.get_key()

    if m == ord('S'):
        print("change flag show")
        flag_show = not flag_show
        time.sleep(0.1)
        robot.get_key()

    if m == 190:
        speed += 10
        print("change speed", speed)
        if speed > 255: speed = 255
        time.sleep(0.3)
        robot.get_key()

    if m == 188:
        speed -= 10
        print("change speed", speed)
        if speed < 0: speed = 0

        time.sleep(0.3)
        robot.get_key()

    if faza == 0:

        frame = robot.get_frame()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        speed_manual = 100
        if m != -1:
            print(m)
        # if flag_move:
        #     robot.move(speed_manual,  speed_manual, 200)
        if m == 37:
            manual_serv = 30
            robot.serv(manual_serv)
            # print(manual_serv)
        if m == 39:
            manual_serv = -30
            robot.serv(manual_serv)
            # print(manual_serv)
        if m == 32:
            manual_serv = 0
            robot.serv(manual_serv)
            # print(manual_serv)
        if m == 38:
            robot.move(speed_manual, speed_manual, 80)
        if m == 40:
            robot.move(-speed_manual, -speed_manual, 80)

        s = robot.speed()

        robot.text_to_frame(frame, "roboracers manual mode ", 20, 20)
        robot.text_to_frame(frame, "manual serv " + str(manual_serv), 20, 50)
        robot.text_to_frame(frame, "speed " + str(robot.speed()), 20, 80)
        robot.text_to_frame(frame, "odometr " + str(round(robot.odometr(), 2)), 20, 100)
        robot.set_frame(frame, 30)

    if faza == 3:
        # настройка фильтра
        frame = robot.get_frame()
        # frame = cv2.resize(frame, (320, 240))
        Y, X, Z = frame.shape

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low, up)
        # mask = cv2.GaussianBlur(mask, (15, 15), 0)

        gray_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        robot.set_frame(gray_image)

        if m == 187:
            up[2] += 1
            time.sleep(0.1)
            robot.get_key()

        if m == 189:
            up[2] -= 1
            time.sleep(0.1)
            robot.get_key()
        if m != -1:
            print(low, up)

    if faza == 1:
        # Движение по додной точке справа
        # работаем только с новыми кадрами
        frame = robot.get_frame(wait_new_frame=True)  # .copy()

        if flag_show:
            frame_show = robot.get_frame()

        Y, X, Z = frame.shape
        X1r = X - int(X / 2.5)
        X2r = X
        Y1r = Y - int(Y / 3.5)
        Y2r = Y

        # frameR = frame[Y1r:Y2r, X1r:X2r].copy()

        hsv = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low, up)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        min_x_r = 100000
        countor_draw = 0
        for contur in contours:
            # мелкие контуры игнорируем
            if cv2.contourArea(contur) > 500:
                x1, y1, w, h = cv2.boundingRect(contur)
                x2 = x1 + w
                y2 = y1 + h
                if x1 < min_x_r:
                    min_x_r = x1
                if x2 < min_x_r:
                    min_x_r = x2
                if flag_show:
                    countor_draw += 1
                    if countor_draw < 3:
                        cv2.line(frame_show, (int(X1r + x2), int(Y1r + y2)), (int(X1r + x1), int(Y1r + y1)),
                                 (0, 255, 0), 3)

        if min_x_r != 100000:
            # точка опоры для регулятора
            porog = 70
            # регулятор. надо менять в зависимости от скорости

            reg_move.set(0.2, 0.02, 0.025)  # (0.2, 0.01, 0.01), (0.2, 0.02, 0.025)

            p = reg_move.apply(porog, min_x_r)
            # print(p)

            if flag_move:
                # выставляем рульь
                robot.serv(p, min=-35, max=35)
                # выставляем скорость
                # внутри три параметра для регуляторпа пайборда которые потдерживают нужную скорость по энкодеру
                # первый параметр скорость, второй сколькко милис. ехать, и PID

                # if speed == 4:ьь
                #     robot.move_fix_speed(speed, 50, p=5, i=0.1, d=1)
                # elif speed == 5:
                #     robot.move_fix_speed(speed, 50, p=10, i=0.1, d=1)
                # elif speed == 6:
                #     robot.move_fix_speed(speed, 50, p=10, i=0.1, d=1)
                # elif speed == 7:
                #     robot.move_fix_speed(speed, 50, p=10, i=0.1, d=1)
                robot.move(speed, 0, 200, wait=False)

            if flag_show:
                cv2.circle(frame_show, (int(X1r + porog), Y1r), 10, (0, 0, 255), 2)
                cv2.circle(frame_show, (X1r + min_x_r, Y1r), 10, (255, 255, 255), 2)
                frame_show = robot.text_to_frame(frame_show, "p: " + str(round(p, 2)), 20, 20)
                frame_show = robot.text_to_frame(frame_show, "speed: " + str(speed), 20, 80)
        else:
            # защита. если робот не видит линию в окошке то он смотрит значение регулятора старое и выкручивает сруль в нужную сторону
            # reg_move.reset()
            if flag_move:
                if p > 0:
                    robot.serv(40, min=-40, max=40)
                if p <= 0:
                    robot.serv(-40, min=-40, max=40)

                robot.move(speed, 0, 200, wait=False)
                # print("zashita")

        if flag_show:
            cv2.rectangle(frame_show, (X1r, Y1r), (X2r, Y2r), (255, 0, 0), 2)
            frame_show = robot.text_to_frame(frame_show, "fps: " + str(fps), 20, 50)

            robot.set_frame(frame_show)
        else:
            robot.set_frame(frame)

    # расчет реального фпс с которым обрабатывается картинка на роботе
    fps_count += 1
    if time.time() - fps_timer > 1:
        fps_timer = time.time()
        # f = open("/sys/class/thermal/thermal_zone0/temp", "r")
        # temp = int(f.readline()) / 1000
        # print( datetime.datetime.now(),temp)
        # print(robot.rc())
        fps = fps_count
        if flag_show == False:
            # print("fps", fps)
            pass
        fps_count = 0
