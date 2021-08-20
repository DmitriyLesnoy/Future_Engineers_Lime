import cv2
import numpy as np
import time
import RobotAPI as rapi
import json
import regulators

robot = rapi.RobotAPI(flag_pyboard=True)
robot.set_camera(100,640,480)

############################################################
# flag_qualification=True


# global_speed = 115
global_speed = 60
pause_finish = 1.7



# пременные порога черной линии
porog_black_line_minus = 275
porog_black_line_plus = 275

# flag_qualification = False
flag_qualification = True
if flag_qualification:
    global_speed = global_speed + 40
    pause_finish = 1
    porog_black_line_plus+=35
    porog_black_line_minus+=35

global_speed_old=global_speed

delta_reg = 0

p=0

delta_green_plus = 20
delta_red_plus = -20

delta_green_minus = 20
delta_red_minus = -20

time_go_back_banka = 500

# global_speed = 0


# state = "Main move"
state = "Manual move"
# state = "Main move"
# state = "HSV"

pause_povorot = 0.7

flag_doezd_r=False
flag_doezd_l=False

timer_finish = None
timer_line=0
flag_line=False

timer_turn_l=0

timer_turn_r=0
############################################################

# 1- по часовой, -1 против часовой стрелки
speed_manual = 100
direction = None
manual_angle = 0
manual_throttle = 0


# low_orange = np.array([0, 50, 80])
# up_orange = np.array([50, 256, 256])
#
# # черный
# low_black = np.array([0, 0, 0])
# up_black = np.array([180, 256, 89])
#
# low_blue = np.array([90, 0, 0])
# up_blue = np.array([120, 256, 170])

class HSV_WORK(object):
    """Work whith hsv colors"""
    colors = {}

    def reset(self):

        print(self.colors)
        self.colors = {
            'orange': [[0, 50, 80], [50, 256, 256]],
            # 'red_low': [[0, 0, 212], [31, 256, 256]],
            #     # 'black_TL': [[0, 0, 0], [256, 256, 86]],
            #     # 'red_STOP_low': [[0, 0, 66], [20, 256, 256]],
            'black': [[0, 0, 0], [180, 256, 89]],
            'green': [[51, 50, 70], [84, 256, 256]],
            'white': [[0, 0, 81], [255, 256, 254]],
            'blue': [[90, 0, 0], [120, 256, 170]],
            #     # 'red_STOP_up': [[149, 0, 150], [256, 256, 256]],
            'red_up': [[96, 0, 0], [255, 256, 256]]
        }

        self.save_to_file()

    def __init__(self):

        self.load_from_file()
        # self.reset()

    def get_color(self, name):
        data = [[0, 0, 0], [256, 256, 256]]
        if isinstance(self.colors, dict):
            if name in self.colors:
                data = self.colors[name]
                # print(green)
        return data

    def constrain(self, x, out_min, out_max):
        if x < out_min:
            return out_min
        elif out_max < x:
            return out_max
        else:
            return x

    def set_color(self, name, data):

        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = self.constrain(data[i][j], 0, 256)
        self.colors[name] = data

    # def save_to_file(self, filename="/home/pi/robot/colors.txt"):
    def save_to_file(self, filename="colors.txt"):
        print("save to file")
        with open(filename, 'w') as outfile:
            json.dump(self.colors, outfile)
        with open(filename + ".copy", 'w') as outfile:
            json.dump(self.colors, outfile)

    # def load_from_file(self, filename="/home/pi/robot/colors.txt"):
    def load_from_file(self, filename="colors.txt"):
        try:
            with open(filename) as json_file:
                self.colors = json.load(json_file)
        except Exception as e:
            print("error load file", e)
            print("load.copy")
            try:
                with open(filename + ".copy") as json_file:
                    self.colors = json.load(json_file)
            except Exception as e1:
                print("failed load copy", e1)

    def make_mask(self, frame, name):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color = self.get_color(name)
        mask = cv2.inRange(hsv, np.array(color[0]), np.array(color[1]))
        # print("make mask", name, color)
        return mask

    def list_names(self):
        names = []
        for i in self.colors:
            names.append(i)
        return names


hsv_work = HSV_WORK()

# текущая стадия программы

old_state = ""
# название стадий
state_names = ["Manual move", "Move to line", "Main move", "Left", "Right"]

# фильтр черного цвета

# low = np.array([0, 0, 00])
# up = np.array([180, 80, 115])

# синий


timer_state = 0


def Find_black_line_left(frame, frame_show, flag_draw=True):
    x1, y1 = 0, 235
    x2, y2 = 30, 480

    # вырезаем часть изображение
    frame_crop = frame[y1:y2, x1:x2]
    frame_crop_show = frame_show[y1:y2, x1:x2]
    # cv2.imshow("frame_crop", frame_crop)
    # рисуем прямоугольник на изображении
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    # mask = cv2.inRange(hsv, low_black, up_black)

    mask = hsv_work.make_mask(frame_crop, "black")
    # выводим маску для проверки
    # cv2.imshow("mask", mask)
    # на отфильтрованной маске выделяем контуры
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры
    flag_line = False
    max_y_left = 0
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 420:
            # отрисовываем найденный контур
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            # включаем зеленый свет
            # robot.lamp.rgb(0, 1, 0)
            if max_y_left < y + h:
                max_y_left = y + h

    cv2.putText(frame_show, "" + str(max_y_left), (0, 210), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 2)
    return max_y_left

def Find_black_line_right(frame, frame_show, flag_draw=True):
    x1, y1 = 640 - 30, 235
    x2, y2 = 640, 480

    # вырезаем часть изображение
    frame_crop = frame[y1:y2, x1:x2]
    frame_crop_show = frame_show[y1:y2, x1:x2]
    # cv2.imshow("frame_crop", frame_crop)
    # рисуем прямоугольник на изображении
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    # mask = cv2.inRange(hsv, low_black, up_black)

    mask = hsv_work.make_mask(frame_crop, "black")
    # выводим маску для проверки
    # cv2.imshow("mask", mask)
    # на отфильтрованной маске выделяем контуры
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры
    flag_line = False
    max_y_right = 0
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 420:
            # отрисовываем найденный контур
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            # включаем зеленый свет
            # robot.lamp.rgb(0, 1, 0)
            if max_y_right < y + h:
                max_y_right = y + h

        cv2.putText(frame_show, "" + str(max_y_right), (600, 210), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 0), 2)
    return max_y_right

def Find_start_line(frame, frame_show, color, flag_draw=True):
    x1, y1 = 320 - 20, 400
    x2, y2 = 320 + 20, 460
    # вырезаем часть изображение
    frame_crop = frame[y1:y2, x1:x2]
    frame_crop_show = frame_show[y1:y2, x1:x2]
    # cv2.imshow("frame_crop", frame_crop)
    # рисуем прямоугольник на изображении
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # переводим изображение с камеры в формат HSV
    # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    # mask = cv2.inRange(hsv, hsv_low, hsv_high)
    mask = hsv_work.make_mask(frame_crop, color)
    # выводим маску для проверки
    # cv2.imshow("mask", mask)
    # на отфильтрованной маске выделяем контуры
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 500:
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            return True

    return False

def Find_box(frame, frame_show, color, flag_draw=True):
    # x1, y1 = 0, 200  # Xanne
    x1, y1 = 0, 100   #Lime
    x2, y2 = 640, 400
    # вырезаем часть изображение
    frame_crop = frame[y1:y2, x1:x2]
    frame_crop_show = frame_show[y1:y2, x1:x2]
    # cv2.imshow("frame_crop", frame_crop)
    # рисуем прямоугольник на изображении

    # переводим изображение с камеры в формат HSV
    # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    # mask = cv2.inRange(hsv, hsv_low, hsv_high)
    mask = hsv_work.make_mask(frame_crop, color)
    # robot.set_frame(mask)
    # выводим маску для проверки
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow("mask", mask)
    # на отфильтрованной маске выделяем контуры
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 300:
            if flag_draw:
                c = (0, 0, 255)
                if color == "green":
                    c = (0, 255, 0)
                cv2.drawContours(frame_crop_show, contour, -1, c, 2)

                cv2.putText(frame_show, str(round(area, 1)), (x + x1, y - 20 + y1),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                            c, 2)
            return x + w / 2, area

    return None, None

def Find_black_box_right(frame, frame_show, color, flag_draw=True):
    x1, y1 = 360, 300
    # x2, y2 = 430, 295
    x2, y2 = 430, 480
    # вырезаем часть изображение
    frame_crop = frame[y1:y2, x1:x2]
    frame_crop_show = frame_show[y1:y2, x1:x2]
    # cv2.imshow("frame_crop", frame_crop)
    # рисуем прямоугольник на изображении
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # переводим изображение с камеры в формат HSV
    # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    # mask = cv2.inRange(hsv, hsv_low, hsv_high)
    mask = hsv_work.make_mask(frame_crop, color)
    # выводим маску для проверки
    # cv2.imshow("mask", mask)
    # на отфильтрованной маске выделяем контуры
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 6000:
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            return True

    return False

def Find_black_box_left(frame, frame_show, color, flag_draw=True):
    x1, y1 = 210, 300
    # x2, y2 = 280, 295
    x2, y2 = 280, 480
    # вырезаем часть изображение
    frame_crop = frame[y1:y2, x1:x2]
    frame_crop_show = frame_show[y1:y2, x1:x2]
    # cv2.imshow("frame_crop", frame_crop)
    # рисуем прямоугольник на изображении
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # переводим изображение с камеры в формат HSV
    # hsv = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    # mask = cv2.inRange(hsv, hsv_low, hsv_high)
    mask = hsv_work.make_mask(frame_crop, color)
    # выводим маску для проверки
    # cv2.imshow("mask", mask)
    # на отфильтрованной маске выделяем контуры
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # перебираем все найденные контуры
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 6000:
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            return True

    return False


robot.wait(500)
# frame1=None
count_lines = 0
e_old = 0
flagfr = 0
index_color = 0
step_hsv = 1
flag_not_save_hsv = 0

hsv_frame = robot.get_frame(wait_new_frame=True)


def put_telemetry(frame_show):
    # вывод телеметрии на экран
    cv2.putText(frame_show, "State: " + state, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 255), 2)
    cv2.putText(frame_show, "Count lines: " + str(count_lines), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 2)
    cv2.putText(frame_show, "Speed: " + str(global_speed), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 0, 255), 2)
    serv,ost=divmod(p,1)
    cv2.putText(frame_show, "Serv: " + str(serv), (10, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 0, 0), 2)
    robot.set_frame(frame_show, 15)


reg_move = regulators.Regulators(0, 0, 0, Ki_border=5)
robot.serv(-35)
robot.serv(0)
robot.sound1()

reg_move.set(0.3, 0.000000001, 0.04)

def go_back(angle, time1, time2):
    global timer_finish
    robot.serv(angle)
    robot.move(-global_speed, 0, time1, wait=False)
    robot.wait(time1)

    robot.serv(-angle)
    robot.move(global_speed, 0, time2, wait=False)
    robot.wait(time2)
    if timer_finish is not None:
        timer_finish += time1 / 1000 + time2 / 1000




while True:
    if robot.button()==1:
        state = "Main move"
    if state != old_state:
        timer_state = time.time()
        old_state = state

    frame = robot.get_frame(wait_new_frame=True)

    frame_show = frame.copy()

    k = robot.get_key()
    # print(k)

    # если нажата клавиша 1
    if k == 48:
        # переключаем програму в 1 стадию
        state = "HSV"
    if k == 49:
        # переключаем програму в 1 стадию
        state = "Manual move"
    # если нажата клавиша 2
    elif k == 50:
        # переключаем програму во 2 стадию
        state = "Move to line"
    elif k == 51:
        # переключаем програму во 2 стадию
        state = "Main move"
        robot.serv(0)
    # elif k == 51:
    #     # переключаем програму в 3 стадию
    #     timer_stop = time.time()
    if k==187:
        global_speed+=1
    elif k==189:
        global_speed-=1
    if k==66:
        robot.tone(3100,300)

    if state == "Manual move":
        # ручное управление

        if k == 37:
            manual_serv = 25
            robot.serv(manual_serv)
            print(manual_serv)
        if k == 39:
            manual_serv = -25
            robot.serv(manual_serv)
            print(manual_serv)
        if k == 32:
            manual_serv = 0
            robot.serv(manual_serv)
            print(manual_serv)
        if k == 38:
            robot.move(speed_manual, 0, 100, wait=False)
        if k == 40:
            robot.move(-speed_manual, 0, 100, wait=False)

        Find_box(frame, frame_show, "green")
        Find_black_box_right(frame, frame_show, "black")
        Find_black_box_left(frame, frame_show, "black")
        # Find_box(frame, "red_up")
        # отправляем команды на робота
        # robot.move(manual_throttle, 0, 100, wait=False)
        # robot.serv(manual_angle)
        # телеметрия ручного управления
        cv2.putText(frame_show, "throttle: " + str(round(manual_throttle, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame_show, "angle: " + str(round(manual_angle, 1)), (10, 80),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        put_telemetry(frame_show)
    elif state == "Main move":

        is_orange = Find_start_line(frame, frame_show, "orange")
        is_blue = Find_start_line(frame, frame_show, "blue")

        if direction==None:
            if is_orange:
                direction = 1
            if is_blue:
                direction = -1

        else:
            if direction==1 and is_orange:
                flag_line=True
                timer_line=time.time()
            if direction==-1 and is_blue:
                flag_line=True
                timer_line=time.time()

            if time.time()>=timer_line+0.05 and flag_line:
                flag_line=False
                count_lines+=1
        if count_lines >= 12:
            # if time.time()>timer_state+1:
            if timer_finish is None:
                timer_finish = time.time() + pause_finish

            else:
                if time.time() > timer_finish:
                    global_speed = 0
                    robot.beep()
                    state = "Finish"

        delta_banka = 0
        delta_speed = 0

        if Find_black_box_left(frame, frame_show, "black") and Find_black_box_right(frame, frame_show, "black"):
            black_box_left, area_left = Find_black_box_left(frame, frame_show, "black")
            black_box_right, area_right = Find_black_box_right(frame, frame_show, "black")
            if area_left>area_right:
                go_back(40, 600, 50)
            else:
                go_back(-40, 600, 50)
        else:
            if Find_black_box_left(frame, frame_show, "black"):
                go_back(40, 600, 50)
            if Find_black_box_right(frame, frame_show, "black"):
                go_back(-40, 600, 50)

        max_y_left = Find_black_line_left(frame, frame_show)
        max_y_right = Find_black_line_right(frame, frame_show)

        delta_reg = max_y_right - max_y_left

        porog=0

        p = reg_move.apply(porog, delta_reg)

        # if max_y_right == 0:
        #     p-=(255-global_speed)/12
        # elif max_y_left==0:
        #     p+=(255-global_speed)/12

        if max_y_right == 0 or flag_doezd_r:
            p=18
            global_speed=80
            if time.time()>=timer_turn_r+0.7:
                p=25
            flag_doezd_r=True
            if 150 > max_y_right>65:
                flag_doezd_r=False
                global_speed=global_speed_old
        else:
            timer_turn_r=time.time()

        if max_y_left==0 or flag_doezd_l:
            p=-22
            global_speed=80
            if time.time()>=timer_turn_l+0.7:
                p=-30
            flag_doezd_l = True
            if 150 > max_y_left > 55:
                flag_doezd_l = False
                global_speed=global_speed_old
        else:
            timer_turn_l=time.time()


        if -5<p<5:
            p=0

        robot.serv(-p + delta_banka)

        robot.move(global_speed,0 , 100, wait=False)

        put_telemetry(frame_show)
    elif state == 'HSV':
        # настройка фильтра HSV
        if flagfr == 0:
            hsv_frame = frame
        Y, X, Z = frame.shape
        lst = hsv_work.list_names()
        name_color = lst[index_color]
        mask = hsv_work.make_mask(hsv_frame, name_color)
        color = hsv_work.colors[name_color]
        low_set, up_set = color[0], color[1]
        gray_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.putText(gray_image, str(name_color), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(gray_image, str(color[0]), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(gray_image, str(color[1]), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(gray_image, "step: " + str(step_hsv), (10, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

        # gray_image = robot.text_to_frame(gray_image, str(name_color), 20, 20, (0, 0, 255), 2)
        # gray_image = robot.text_to_frame(gray_image, str(color[0]), 170, 20, (0, 0, 255), 2)
        # gray_image = robot.text_to_frame(gray_image, str(color[1]), 170, 45, (0, 0, 255), 2)
        # gray_image = robot.text_to_frame(gray_image, "step: " + str(step_hsv), 20, gray_image.shape[0] - 20,
        #                                  (0, 0, 255), 2)
        if flag_not_save_hsv:
            pass
            # cv2.putText(gray_image, str("need save hsv"), (120, gray_image.shape[0] - 50),
            #             cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 6)

        robot.set_frame(gray_image)
        # cv2.imshow("hsv", gray_image)
        m = k
        if m == 32: flagfr = not flagfr

        if m == 81: low_set[0] -= step_hsv
        if m == 87: low_set[0] += step_hsv
        if m == 69: up_set[0] -= step_hsv
        if m == 82: up_set[0] += step_hsv
        if m == 65: low_set[1] -= step_hsv
        if m == 83: low_set[1] += step_hsv
        if m == 68: up_set[1] -= step_hsv
        if m == 70: up_set[1] += step_hsv
        if m == 90: low_set[2] -= step_hsv
        if m == 88: low_set[2] += step_hsv
        if m == 67: up_set[2] -= step_hsv
        if m == 86: up_set[2] += step_hsv

        if m >= 65 and m <= 90:
            flag_not_save_hsv = True

        hsv_work.set_color(name_color, [low_set, up_set])
        if m == 8:
            if step_hsv == 1:
                step_hsv = 10
            else:
                step_hsv = 1
        if m == 13:
            hsv_work.save_to_file()
            flag_not_save_hsv = False

        if m == 40:  # вниз
            index_color += 1
            lst = hsv_work.list_names()
            if index_color >= len(lst):
                index_color = 0
            robot.wait(200)
            robot.get_key()

        if m == 38:  # вверх
            index_color -= 1
            lst = hsv_work.list_names()
            if index_color < 0:
                index_color = len(lst) - 1
            robot.wait(200)
            robot.get_key()

        name_color = lst[index_color]
        color = hsv_work.colors[name_color]
        low_set, up_set = color[0], color[1]

        if m != -1:
            print(name_color, low_set, up_set)
            print(m)

        pass
