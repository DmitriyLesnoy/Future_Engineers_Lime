import cv2
import numpy as np
import time
import RobotAPI as rapi
import json
import regulators

#импорт необходимых библиотек

robot = rapi.RobotAPI(flag_pyboard=True)
robot.set_camera(100,640,480)
#инициализация камеры

############################################################
# flag_qualification=True


# global_speed = 115
global_speed = 60
pause_finish = 1.2
#установка скорости и времени финиша

# пременные порога черной линии
porog_black_line_minus = 270
porog_black_line_plus = 310

# flag_qualification = False
flag_qualification = False
if flag_qualification:
    global_speed = global_speed + 60
    pause_finish = 0.3
    porog_black_line_plus+=35
    porog_black_line_minus+=35
#установка значений для квалификации и основного задания


delta_green_plus = 22
delta_red_plus = -22

delta_green_minus = 18
delta_red_minus = -18

time_go_back_banka = 500
#установка значений для красных и зеленых кубиков

# global_speed = 0


# state = "Main move"
state = "Manual move"
# state = "Main move"
# state = "HSV"

pause_povorot = 0.7


timer_finish = None
############################################################

# 1- по часовой, -1 против часовой стрелки
speed_manual = 100
direction = 0
manual_angle = 0
manual_throttle = 0
#обнуление переменных

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
#класс фильтрации цветов

hsv_work = HSV_WORK()

# текущая стадия программы

old_state = ""
# название стадий
state_names = ["Manual move", "Move to line", "Main move", "Left", "Right"]
#стадии алгоритма
# фильтр черного цвета

# low = np.array([0, 0, 00])
# up = np.array([180, 80, 115])

# синий


timer_state = 0


def Find_black_line(frame, frame_show, direction, flag_draw=True):
    x1, y1 = 640 - 20, 0
    x2, y2 = 640, 480

    if direction == 1:
        x1, y1 = 0, 0
        x2, y2 = 20, 480

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
    max_y = 0
    for contour in contours:
        # Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        # вычисляем площадь найденного контура
        area = cv2.contourArea(contour)
        if area > 20:
            # отрисовываем найденный контур
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            # включаем зеленый свет
            # robot.lamp.rgb(0, 1, 0)
            if max_y < y + h:
                max_y = y + h
    return max_y
#функцияя поиска черного бортика поля

def Find_start_line(frame, frame_show, color, flag_draw=True):
    x1, y1 = 320 - 20, 400
    x2, y2 = 320 + 20, 440
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
        if area > 350:
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            return True

    return False
#функция поиска стартовой линии

def Find_box(frame, frame_show, color, flag_draw=True):
    # x1, y1 = 0, 200  # Xanne
    x1, y1 = 0, 200   #Lime
    x2, y2 = 640, 460
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
        if area > 700:
            if flag_draw:
                c = (0, 0, 255)
                if color == "green":
                    c = (0, 255, 0)
                cv2.drawContours(frame_crop_show, contour, -1, c, 2)

                cv2.putText(frame_show, str(round(area, 1)), (x + x1, y - 20 + y1),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,c, 2)
            return x + w / 2, area

    return None, None
#функция поиска кубиков

def Find_black_box_right(frame, frame_show, color, flag_draw=True):
    x1, y1 = 360, 290
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
        if area > 2800:
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            return True

    return False
#функция поиска черного бортипа перед роботом справа

def Find_black_box_left(frame, frame_show, color, flag_draw=True):
    x1, y1 = 210, 290
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
        if area > 2800:
            if flag_draw:
                cv2.drawContours(frame_crop_show, contour, -1, (0, 0, 255), 2)
            return True

    return False
#функция поиска черного бортипа перед роботом слева

robot.wait(500)
# frame1=None
count_lines = 0
e_old = 0
flagfr = 0
index_color = 0
step_hsv = 1
flag_not_save_hsv = 0
#обнуление переменных
hsv_frame = robot.get_frame(wait_new_frame=True)
#установка изображения для работы класса НSV

def put_telemetry(frame_show):
    # вывод телеметрии на экран
    cv2.putText(frame_show, "State: " + state, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 255), 2)
    cv2.putText(frame_show, "Count lines: " + str(count_lines), (10, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 2)
    cv2.putText(frame_show, "Speed: " + str(global_speed), (10, 120), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 0, 255), 2)

    robot.set_frame(frame_show, 15)
#функция вывода надписей на экран

reg_move = regulators.Regulators(0, 0, 0, Ki_border=5)
robot.serv(-35)
robot.serv(0)
robot.sound1()
#установка значений для регулятора

def go_back(angle, time1, time2):
    global timer_finish
    robot.serv(angle)
    robot.move(-global_speed-40, 0, time1, wait=False)
    robot.wait(time1)

    robot.serv(-angle)
    robot.move(global_speed, 0, time2, wait=False)
    robot.wait(time2)
    if timer_finish is not None:
        timer_finish += time1 / 1000 + time2 / 1000
#функция движения назад для объезда препядствий


while True:
    if robot.button()==1:
        state = "Move to line"
    if state != old_state:
        timer_state = time.time()
        old_state = state

    frame = robot.get_frame(wait_new_frame=True)
    # получение с камеры робота изображение
    frame_show = frame.copy()
    # копирование получаемого  камеры изображения
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
    #определенные действия при наатии определенных кнопок
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
        #ручное управление кнопкамии на клавиатуре компьютера
        Find_box(frame, frame_show, "green")
        Find_black_box_right(frame, frame_show, "black")
        Find_black_box_left(frame, frame_show, "black")
        cv2.putText(frame_show, "throttle: " + str(round(manual_throttle, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame_show, "angle: " + str(round(manual_angle, 1)), (10, 80),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        #вывод телеметрии
        put_telemetry(frame_show)
        # вывод телеметрии
    elif state == "Move to line":
        # стадия движения до линии
        robot.serv(0)
        robot.move(global_speed, 0, 100, wait=False)
        # выставлении сервомотора ровно
        is_orange = Find_start_line(frame, frame_show, "orange")
        is_blue = Find_start_line(frame, frame_show, "blue")
        #поиск оранжевой и синей линий
        # print("orange:",is_orange, "Blue:", is_blue)

        if is_orange:
            direction = 1
            state = "Right"
            print("End state Move to line, go ", state)
        #поиск оранжевого
        if is_blue:
            direction = -1
            state = "Left"
            # frame1 = frame
            print("End state Move to line, go ", state)
         # поиск оранжевого
        #результат вычислений
        put_telemetry(frame_show)
        #вывод телеметрии
    elif state == "Left":
        #стади повората влево
        cv2.putText(frame_show, "timer: " + str(round(time.time() - timer_state, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        #вывод телеметрии
        if time.time() < timer_state + pause_povorot:
            robot.move(global_speed, 0, 100, wait=False)
            robot.serv(30)
        # едем прямо, а потом переключаемся в 1 стадию
        if time.time() > timer_state + pause_povorot:
            state = "Main move"
        # таймер поворота
        is_orange = Find_start_line(frame, frame_show, "orange")
        #поис оранжевой линии
        if is_orange:
            state = "Main move"
        # при её обнаружении переключаемся в стадию движения
        put_telemetry(frame_show)
        #вывод телеметрии
    elif state == "Right":
        cv2.putText(frame_show, "timer: " + str(round(time.time() - timer_state, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        #вывод телеметрии
        if time.time() < timer_state + pause_povorot:
            robot.move(global_speed, 0, 100, wait=False)
            robot.serv(-30)
        # едем прямо, а потом переключаемся в 1 стадию
        if time.time() > timer_state + pause_povorot:
            state = "Main move"
        # таймер поворота
        put_telemetry(frame_show)
        # вывод телеметрии
    elif state == "Main move":
        #стадия движения
        if count_lines >= 11:
            if timer_finish is None:
                timer_finish = time.time() + pause_finish
        #счетчик пворотов, при прозождении 12 поворотов робот засекает таймер финиша
            else:
                if time.time() > timer_finish:
                    global_speed = 0
                    robot.beep()
                    state = "Finish"
                    #переход в стадию финиша
        delta_banka = 0
        delta_speed = 0
        #обнуление переменных
        if direction == 1:
        # если напрвление двиения по часовой стрелке
            if Find_black_box_left(frame, frame_show, "black"):
                go_back(40, 250, 100)
            #робот остерегается черного бортика слева
            is_orange = Find_start_line(frame, frame_show, "orange")
            if is_orange:
                state = "Right"
                count_lines += 1
            #если робот замечает оранжевую линию он прибавляет к счетчику поворотов 1 и переключается в стадию поворота направо
            if not flag_qualification:
                cord_red_banka, area_red_banka = Find_box(frame, frame_show, "red_up")
                # если робот едет основное задание он ищет красные банки и записыват их положение и площадь  в пикселях
                if area_red_banka is not None:
                    delta_banka = delta_red_plus
                    if area_red_banka > 13500:
                        go_back(40, time_go_back_banka, 120)
                #если банка слишком близко к роботу - он включает защиту и оъезжает он нее назад

                cord_green_banka, area_green_banka = Find_box(frame, frame_show, "green")
                # если робот едет основное задание он ищет зеленые банки и записыват их положение и площадь  в пикселях
                if area_green_banka is not None:
                    delta_banka = delta_green_plus
                    # print(area_green_banka)
                    if area_green_banka > 13500:
                        go_back(-40, time_go_back_banka, 120)
                #если банка слишком близко к роботу - он включает защиту и оъезжает он нее назад

                if area_green_banka is not None and area_red_banka is not None:

                    if area_red_banka > area_green_banka:
                        delta_banka = delta_red_plus
                    else:
                        delta_banka = delta_green_plus
                # если робот обнаружил сразу 2 банки - он определяет какакя из них больше и ставит её в рпиоретет

        if direction == -1:
        # если напрвление двиения против часовой стрелки
            if Find_black_box_right(frame, frame_show, "black"):
                go_back(-40, 250, 100)
            # робот остерегается черного бортика справа
            is_blue = Find_start_line(frame, frame_show, "blue")
            if is_blue:
                state = "Left"
                count_lines += 1
            # если робот замечает оранжевую синию он прибавляет к счетчику поворотов 1 и переключается в стадию поворота налево
            if not flag_qualification:
                cord_red_banka, area_red_banka = Find_box(frame, frame_show, "red_up")
                # если робот едет основное задание он ищет зеленые банки и записыват их положение и площадь  в пикселях
                if area_red_banka is not None:
                    delta_banka = delta_red_minus
                    if area_red_banka > 12700:
                        go_back(40, time_go_back_banka, 120)
                # если банка слишком близко к роботу - он включает защиту и оъезжает он нее назад
                cord_green_banka, area_green_banka = Find_box(frame, frame_show, "green")
                # если робот едет основное задание он ищет красные банки и записыват их положение и площадь  в пикселях
                if area_green_banka is not None:
                    delta_banka = delta_green_minus
                    # print(area_green_banka)
                    if area_green_banka > 12700:
                        go_back(-40, time_go_back_banka, 120)
                # если банка слишком близко к роботу - он включает защиту и оъезжает он нее назад
                if area_green_banka is not None and area_red_banka is not None:

                    # delta_speed = -10

                    if area_red_banka > area_green_banka:
                        delta_banka = delta_red_minus
                    else:
                        delta_banka = delta_green_minus
                # если робот обнаружил сразу 2 банки - он определяет какакя из них больше и ставит её в рпиоретет

        max_y = Find_black_line(frame, frame_show, direction)
        # робот определяет высоту от нижнего края экрана до нижней точки видимого контура в границах в зависимоссти от направления
        if max_y > 0:
            reg_move.set(0.4, 0.00001, 0.08)
            # если высота положительна то робот едет по pid регулятору
            porog = porog_black_line_minus
            if direction > 0:
                porog = porog_black_line_plus
            # робот выберает порог в зависимости от направления движения

            p = reg_move.apply(porog, max_y) * direction
            robot.serv(p + delta_banka)
            # робот вычесляет необ ходимый поворот и отправляет на сервопривод
            robot.move(global_speed + delta_speed, 0, 100, wait=False)
            # включение двигателя на определенную скорость
        else:
            if direction == -1:
                go_back(50, 370, 200)
            else:
                go_back(-50, 370, 200)
            # в зависимости от направления робот отъезжает назад чтобы не было столкновения с бортиком
        put_telemetry(frame_show)
        # вывод телеметрии
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
        # создание маски для работы фиильтра HSV
        gray_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.putText(gray_image, str(name_color), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(gray_image, str(color[0]), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(gray_image, str(color[1]), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        cv2.putText(gray_image, "step: " + str(step_hsv), (10, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)
        # вывод телеметрии
        if flag_not_save_hsv:
            pass

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
        # управление настройками фильтра клавиаатуррой компьютера
        hsv_work.set_color(name_color, [low_set, up_set])
        if m == 8:
            if step_hsv == 1:
                step_hsv = 10
            else:
                step_hsv = 1
        if m == 13:
            hsv_work.save_to_file()
            flag_not_save_hsv = False
        # сохранение значчений фильтра для дальнейшей работы
        if m == 40:  # вниз
            index_color += 1
            lst = hsv_work.list_names()
            if index_color >= len(lst):
                index_color = 0
            robot.wait(200)
            robot.get_key()
        # перелистывание списка настройки цветов вниз
        if m == 38:  # вверх
            index_color -= 1
            lst = hsv_work.list_names()
            if index_color < 0:
                index_color = len(lst) - 1
            robot.wait(200)
            robot.get_key()
        # перелистывание списка настройки цветов вверх
        name_color = lst[index_color]
        color = hsv_work.colors[name_color]
        low_set, up_set = color[0], color[1]

        if m != -1:
            print(name_color, low_set, up_set)
            print(m)
            # вывод полученных значений
        pass
