import cv2
import numpy as np
import time
import RobotAPI as rapi
import json
import regulators

# импорт необходимых библиотек
from INGENEERS import reg_move

robot = rapi.RobotAPI(flag_pyboard=True) # инициализация робота
robot.set_camera(100,640,480) # инициализация камеры

flag_qualification=False # установление флага квалификации на значение ложь

global_speed = 70 # установление скорости езды робота

global_speed_old=global_speed # утсановление значения переменной для сорости

pause_finish=90/global_speed # установление паузы финиша

delta_reg = 0 # обнуление переменной разности датчиков

p=0 # обнуление переменной регулятора
delta_reg_old=0 # обнудение переменнйо прошлого показания delta_reg
delta_banka=0 # обнуление перемменной объезда дорожных знаков

state = "Manual move" # начальная стадия программы


povorot = False # обнуление фалага экстренного поворота

flag_doezd_r=False # обнуление флага поворота направо
flag_doezd_l=False # обнуление флага поворота налево

timer_finish = None # обнуление таймера финиша
timer_line=0 # обнуление счетчика поворотов
flag_line=False # обнуление флага онаружающего линию поворота

timer_turn_l=0 # обнуление таймераа поворота налево
timer_turn_r=0 # обнуление таймера поворота направо

timer_sec=None  # обнуление таймера секундомера
secundomer=0  # обнуление переменной секундомера

timer_banka=0 # обнуление таймера объезда дорожного знака

green=False # обнулене флага зеленого дорожого знака
red=False # обнуение флага красного дорожного знака

speed_manual = 100 # задача значения переменной скорости ля ручного управления
direction = None # обнуление значенияя переменной напавления движения
manual_angle = 0 # обнуление переменной поворота сервомотора на ручном управлении
manual_throttle = 0 # обнуление переменной движения ведущего мотора на ручнм управвлении

class HSV_WORK(object):
    # класс работы с цветами HSV
    """Work whith hsv colors"""
    colors = {}

    def reset(self):
        # перезагрузка значений HSV
        print(self.colors)
        self.colors = {
            'orange': [[0, 50, 80], [50, 256, 256]],
            'black': [[0, 0, 0], [180, 256, 89]],
            'green': [[51, 50, 70], [84, 256, 256]],
            'white': [[0, 0, 81], [255, 256, 254]],
            'blue': [[90, 0, 0], [120, 256, 170]],
            'red_up': [[96, 0, 0], [255, 256, 256]]
        }

        self.save_to_file()

    def __init__(self):
        # инициаль=изация
        self.load_from_file()
        # self.reset()

    def get_color(self, name):
        # функция получения маски цвета
        data = [[0, 0, 0], [256, 256, 256]]
        if isinstance(self.colors, dict):
            if name in self.colors:
                data = self.colors[name]
                # print(green)
        return data

    def constrain(self, x, out_min, out_max):
        # функция установления минимального и максимального выходного значений
        if x < out_min:
            return out_min
        elif out_max < x:
            return out_max
        else:
            return x

    def set_color(self, name, data):
        # установление цвета
        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = self.constrain(data[i][j], 0, 256)
        self.colors[name] = data

    def save_to_file(self, filename="colors.txt"):
        # функция сохранения значений в файл
        print("save to file")
        with open(filename, 'w') as outfile:
            json.dump(self.colors, outfile)
        with open(filename + ".copy", 'w') as outfile:
            json.dump(self.colors, outfile)

    def load_from_file(self, filename="colors.txt"):
        # функция загрузки данных из файла
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
        # функция создания маски цвета
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color = self.get_color(name)
        mask = cv2.inRange(hsv, np.array(color[0]), np.array(color[1]))
        # print("make mask", name, color)
        return mask

    def list_names(self):
        # функция вывода списка цветов
        names = []
        for i in self.colors:
            names.append(i)
        return names

hsv_work = HSV_WORK() # присвоение класса работы с HSV цветами

old_state = ""  # задача значений прошлой стадии программы
fps=0 # обнуление счетчика fps
fps_result=0 # переменная отображающая рузельтат подсчета fps
fps_timer=0 # таймера для расчета fps

timer_state = 0 # таймера стадии робота

def Find_black_line_left(frame_show, flag_draw=True):
    # функция поиска черного бортика слева

    d=0
    if direction==1:
        d=30

    x1, y1 = 0, 230-d
    x2, y2 = 20, 380

    frame_crop_show = frame_show[y1:y2, x1:x2]# вырезаем часть изображение

    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2)# рисуем прямоугольник на изображении
    mask = hsv_work.make_mask(frame_crop_show, "black") # применяем маску для проверки
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # на отфильтрованной маске выделяем контуры

    flag_line = False
    max_y_left = 0
    for contour in contours: # перебираем все найденные контуры

        x, y, w, h = cv2.boundingRect(contour) # Создаем прямоугольник вокруг контура

        area = cv2.contourArea(contour) # вычисляем площадь найденного контура
        if area > 400:
            if flag_draw: # отрисовываем найденный контур прямоугольником
                cv2.rectangle(frame_crop_show, (x, y), (x+w, y+h), (0, 0, 255), 2)
            if max_y_left < y + h:
                max_y_left = y + h

    cv2.putText(frame_show, "" + str(max_y_left), (0, 210), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 2)
    return max_y_left-d

def Find_black_line_right(frame_show, flag_draw=True):
    # функция поиска черного бортика справа

    d=0
    if direction==-1:
       d=30

    x1, y1 = 640 - 20, 230-d
    x2, y2 = 640, 380


    frame_crop_show = frame_show[y1:y2, x1:x2] # вырезаем часть изображение
    mask = hsv_work.make_mask(frame_crop_show, "black") # применяем маску для проверки
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # на отфильтрованной маске выделяем контуры
    flag_line = False
    max_y_right = 0
    for contour in contours: # перебираем все найденные контуры
        x, y, w, h = cv2.boundingRect(contour) # Создаем прямоугольник вокруг контура
        area = cv2.contourArea(contour) # вычисляем площадь найденного контура
        if area > 400:
            if flag_draw: # отрисовываем найденный контур
                cv2.rectangle(frame_crop_show, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if max_y_right < y + h:
                max_y_right = y + h
        cv2.putText(frame_show, "" + str(max_y_right), (600, 210), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 255, 0), 2)
    return max_y_right-d

def Find_start_line(frame_show, color, flag_draw=True):
    # функция поиска линии поворота

    x1, y1 = 320 - 20, 440
    x2, y2 = 320 + 20, 480

    frame_crop = frame_show[y1:y2, x1:x2] # вырезаем часть изображение
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 255), 2) # рисуем прямоугольник на изображении
    mask = hsv_work.make_mask(frame_crop, color) # применяем маску для проверки
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # на отфильтрованной маске выделяем контуры
    for contour in contours: # перебираем все найденные контуры

        x, y, w, h = cv2.boundingRect(contour) # Создаем прямоугольник вокруг контура

        area = cv2.contourArea(contour) # вычисляем площадь найденного контура
        if area > 200:
            if flag_draw:
                cv2.rectangle(frame_crop, (x, y), (x+w, y+h), (255, 0, 0), 2)
            return True

    return False

def Find_box(frame_show, flag_draw=True):
    # фугкция поиска дорожных знаков

    x1, y1 = 60, 250
    x2, y2 = 640-60, 400
    frame_crop_show = frame_show[y1:y2, x1:x2] # вырезаем часть изображение
    cv2.rectangle(frame_show, (x1, y1), (x2, y2), (0, 255, 0), 2) # рисуем прямоугольник на изображении
    frame_crop=cv2.GaussianBlur(frame_crop_show,(5,5),cv2.BORDER_DEFAULT) # делаем размытие по гауссу

    y_old=0
    color = "red_up"  # установление цвета знака который нужно найти
    x_red_banka = None # обнуление х координаты красного знака
    y_red_banka = None # обнуление у координаты красного знака
    area_red_banka = None # обнуление площади красного знака

    maskr = hsv_work.make_mask(frame_crop, color) # применяем маску для проверки
    _, contours, hierarchy = cv2.findContours(maskr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # на отфильтрованной маске выделяем контуры

    for contour in contours: # перебираем все найденные контуры
        x, y, w, h = cv2.boundingRect(contour) # Создаем прямоугольник вокруг контура
        area = cv2.contourArea(contour) # вычисляем площадь найденного контура
        if area > 900:
            if y_old<y+h:
                y_old=y+h
                if x+w/2>275:
                    x_red_banka = int(x+(abs(275-(x+w/2))/225)*(150-(y+h))/2)
                else:
                    x_red_banka = int((x+w)-(abs(275-(x+w/2))/225)*(150-(y+h))/2)

                y_red_banka = y + h
                area_red_banka = area
                if flag_draw:
                    c = (0, 0, 255)
                    if color == "green":
                        c = (0, 255, 0)
                    cv2.rectangle(frame_crop_show, (x, y), (x + w, y + h), c, 2)
                    cv2.putText(frame_show, str(round(area, 1)), (x + x1, y - 20 + y1),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,c, 2)
                    cv2.putText(frame_show, str(x_red_banka)+ " " +str(y_red_banka), (x + x1, y - 40 + y1),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255), 2)

    color = "green"
    x_green_banka = None # обнуление х координаты зеленого знака
    y_green_banka = None # обнуление у координаты зеленого знака
    area_green_banka = None # обнуление площади зеленого знака
    maskg = hsv_work.make_mask(frame_crop_show, color) # применяем маску для проверки
    _, contours, hierarchy = cv2.findContours(maskg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # на отфильтрованной маске выделяем контуры

    for contour in contours: # перебираем все найденные контуры
        x, y, w, h = cv2.boundingRect(contour) # Создаем прямоугольник вокруг контура
        area = cv2.contourArea(contour) # вычисляем площадь найденного контура
        if area > 900:
            if y_old<y+h:
                y_old=y+h
                if x+w/2>275:
                    x_green_banka = int(x+(abs(275-(x+w/2))/225)*(150-(y+h))/2)
                else:
                    x_green_banka = int(x+w - (abs(275-(x+w/2))/225)*(150-(y+h))/2)
                y_green_banka = y + h
                area_green_banka = area
                if flag_draw:
                    c = (0, 0, 255)
                    if color == "green":
                        c = (0, 255, 0)
                    cv2.rectangle(frame_crop_show, (x, y), (x + w, y + h), c, 2)
                    cv2.putText(frame_show, str(round(area, 1)), (x + x1, y - 20 + y1),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, c, 2)
                    cv2.putText(frame_show, str(x_green_banka)+ " " +str(y_green_banka), (x + x1, y - 40 + y1),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)


    return x_red_banka, y_red_banka, area_red_banka, x_green_banka, y_green_banka, area_green_banka  # возвращение значений


robot.wait(500) # задержка
count_lines = 0  # обнудение псчетчика линий поворота
flagfr = 0 # обнуление флага кадра с  робота
index_color = 0 # обнуление индекса цвета для фильтра HSV
step_hsv = 1 # задача изменение значение для фильтра HSV
flag_not_save_hsv = 0 # обнуление переменной созранения значений HSV

porog=0  # обнуление порога регулятора

hsv_frame = robot.get_frame(wait_new_frame=True)  # ожидание нового кадра для фильтра HSV


def put_telemetry(frame_show):
    # вывод телеметрии на экран
    cv2.putText(frame_show, "Count lines: " + str(count_lines), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 255, 255), 2)
    cv2.putText(frame_show, "Speed: " + str(global_speed), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 255, 255), 2)
    cv2.putText(frame_show, "Serv: " + str(p), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 255, 255), 2)
    cv2.putText(frame_show, "rt-lf=: " + str(delta_reg), (10,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 255, 255), 2)
    cv2.putText(frame_show, "Time: " + str(secundomer), (500, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 255, 255), 2)
    cv2.putText(frame_show, "dir: " + str(direction), (200, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (255, 255, 255), 2)
    robot.set_frame(frame_show, 40)

robot.serv(-35) # установление сервомотора на -35 градусов
robot.serv(0) # выравнивание срвомотора на 0 градусов
robot.sound1() # звук загрузки программы робота

reg_move.set(0.3, 0, 0.1) # установление коэффициентов регулятора пд

def go_back(angle, time1, time2):
    # функция отъезда назад
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
    if robot.button()==1: # ожидание нажатия кнопки старта робота
        state = "Main move" # установление стадии программы
    if state != old_state:
        timer_state = time.time()
        old_state = state

    frame_show = robot.get_frame(wait_new_frame=1) # получение изображения с робота

    if state == "Main move":
        # стадия самостоятельного движения
        if timer_sec==None: # начало отсчета секундомера
            timer_sec=time.time()
        secundomer=time.time()-timer_sec

        is_orange = Find_start_line(frame_show, "orange") # поиск орнжевой линии поворота
        is_blue = Find_start_line(frame_show, "blue") # поиск синей линии поворота

        if direction==None: # если направление роботу еще не известно
            if is_orange: # если робот нашел оранжевую линию
                direction = 1 # значит направление по часовой стрелке
                porog=0 # порог равен 0
            if is_blue: # если робот нашел синюю линиб поворота
                direction = -1 # значит направление против часовой стрелки
                porog=30 # порог равен 30

        else: # если робот знает направление движения
            if direction==1 and is_orange: # если направление движения по часовой стрелке и он увидел орандевую линию
                flag_line=True # флаг линии равен истина
                timer_line=time.time() # засекается таймер линии
            if direction==-1 and is_blue: # если направление движения против часовой стрелке и он увидел синию линию
                flag_line=True # флаг линии равен истина
                timer_line=time.time() # засекается таймер линии

            if time.time()>=timer_line+0.1 and flag_line: # если прошла 0.1 секунда и робот до этого видел линию
                flag_line=False # флаг линии становится ложь
                count_lines+=1 # счетчик линий становтся на 1 больше

        if count_lines >= 12: # елси робот проехал 12 поворотов=3круга
            if timer_finish is None: # если таймер финиша еще не засечен
                timer_finish = time.time() + pause_finish # засекаем таймер финиша с учетом паузы виниша

            else: # если таймер финиша уже засечен
                if time.time() >= timer_finish: # если таймер финиша вышел
                    global_speed_old = global_speed # запоминаем текущую скорость
                    global_speed = -2 # скорость устанавливаем -2
                    robot.serv(0) # выравниваем сервомотор
                    robot.move(-5,0,2,wait=True) # робот тормозит
                    robot.beep() # робот издает сигнал о финишировании
                    state = "Finish" # стадия финиша

        delta_banka = 0 # обнуление значения обруливания дорожного знака
        delta_red = 0 # обнуление переменной обруливания красного знака
        delta_green = 0 # обнуление переменной обруливания зеленого знака


        x_red_banka, y_red_banka, area_red_banka, x_green_banka, y_green_banka, area_green_banka= Find_box(frame_show) # получение данных о дорожных знаках
        if area_red_banka is not None: # если робот обнаружил красный знак
            red=True # флаг красного знака - истина

            if x_red_banka>275: # если х координата красного знака больше 275
                delta_red=40 # бруливание красного знака = 40
            elif x_red_banka<120: # если х координата красного знака меньше 120
                delta_red = 0 # обруливание красного знака = 0
            else:
                delta_red=40-(275-x_red_banka)/3.3  # иначе обруливание от красного знака расчитывается по формуле
            if direction==1: # если направление по часовой стрелке
                delta_banka = delta_red+y_red_banka/6 # к обруливанию дорожного знака прибавляется поворот от красного знака по формуле от у координаты красного знака
            else:
                delta_banka = delta_red + y_red_banka /2 # к обруливанию дорожного знака прибавляется меньший поворот от красноо знака по формуле от у координаты красного знака
            if delta_banka > 60: # если обруливание знака больше 60
                delta_banka = 60 # обруливание знака = 60
            delta_banka=delta_banka*-1 # значение обруливание знака умножается на -1
        if area_green_banka is not None: # если робот обнаружил зеленый знак
            green=True # флаг зеленого знака - истина
            if x_green_banka<275: # если х координата зеленого знака меньше 275
                delta_green=40 # бруливание зеленого знака = 40
            elif x_green_banka>370: # если х координата зеленого знака больше 370
                delta_green = 0 # обруливание зеленого знака = 0
            else:
                delta_green=40-(x_green_banka-275)/3.3  # иначе обруливание от зеленого знака расчитывается по формуле
            if direction==-1: # если направление против часовой стрелки
                delta_banka = delta_green+y_green_banka/6 # к обруливанию дорожного знака прибавляется поворот от зеленого знака по формуле от у координаты зеленого знака
            else:
                delta_banka = delta_green + y_green_banka /2 # к обруливанию дорожного знака прибавляется меньший поворот от зеленого знака по формуле от у координаты зеленого знака
            if delta_banka > 60: # если обруливание знака больше 60
                delta_banka = 60 # обруливание знака = 60

        if area_green_banka is not None and area_red_banka is not None: # если робот нашел и зеленый и красный дорожный знаки
            if area_red_banka > area_green_banka: # если площадь в пикселях красного знака больше площади зеленого знака
                delta_banka = delta_red # обруливание от знака равно обруливанию красного знака
                green=False # флаг зеленого знака равен ложь
            else: # иначе
                delta_banka = delta_green # обруливание от знака равно обруливанию зеленого знака
                red=False # флаг крсного знака равен ложь

        # вывод на экран значения отруливания от дорожного знака
        cv2.putText(frame_show, "banka: " + str(delta_banka), (10, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (255, 255, 255), 2)

        max_y_left = Find_black_line_left(frame_show) # поиск левого черного бортика поля
        max_y_right = Find_black_line_right(frame_show) # поиск правого черного бортика поля

        if max_y_right>0 and max_y_left>0: # если оба датчика не видят бортик
            green=False # флаг зелегоно знака равен ложь
            red=False # флаг красного знака равен ложь

        delta_reg = max_y_right - max_y_left + porog  # расчитывание разницы показаний датчиков и суммы отдаления от центра
        p = int(delta_reg * 0.5 + (delta_reg - delta_reg_old) * 0.2) # расчитывание ошибки
        delta_reg_old = delta_reg # присваивание переменной значения ошибки


        if (max_y_right == 0 or flag_doezd_r) and not flag_doezd_l: # если правый датчик не видит линию или флаг доезда направо истина и при этом флаг доезда налево ложь
            if time.time()<=timer_turn_r+0.8:  # если таймер поворота направо на 0.8 секунд не истек
                p=-20 # ошибка равна -20
            else: # иначе
                p=-55 # ошибка равна -55
            if povorot: # если флаг экстренного поворота истина
                p=-55 # ошибка равна -55

            if direction==1 and green: # если напрвление по часовой стрелке и флаг зеленого истина
                p=-55 # ошибка равна -55
            flag_doezd_r=True # флаг доезд направо истина

            if direction==1: # если направление по часовой стрелке
                if max_y_right > 40 and time.time()>timer_turn_r+0.4: # если показание правого датчика больше 40 и таймер поворота направо на 0.4 секуны истек
                    flag_doezd_r = False # флаг доезд направго ложь
                    povorot = False # флаг экстренного поворота ложь
            else: # иначе
                if max_y_right > 40: # если показание правого датчика больше 40
                    flag_doezd_r = False # флаг доезда направо ложь
                    povorot = False # флаг экстренного поворота ложь
            if direction == -1 and max_y_left == 0: # если направление против часовой стрелки и показание левого датчика = 0
                flag_doezd_r=False # флаг доезда направо ложь
                flag_doezd_l=True # флаг доезда налево истина
                povorot=True # флаг экстренного поворота истина
        else: # иначе
            timer_turn_r=time.time()  # обновляем таймер поворота направо

        if (max_y_left==0 or flag_doezd_l) and not flag_doezd_r: # если левый датчик не видит линию или флаг доезда налево истина и при этом флаг доезда направо ложь
            if time.time()<=timer_turn_l+0.8:  # если таймер поворота налево на 0.8 секунд не истек
                p=25 # ошибка равна 25
            else: # иначе
                p=55 # ошибка равна 55
            if povorot: # если флаг экстренного поворота истина
                p=55 # ошибка равна 55
            if direction==-1 and red: # если напрвление против часовой стрелки и флаг красного истина
                p=55 # ошибка равна 55
            flag_doezd_l = True # флаг доезд налево истина

            if direction==-1: # если направление против часовой стрелки
                if max_y_left > 40 and time.time()>timer_turn_l+0.4: # если показание левого датчика больше 40 и таймер поворота налево на 0.4 секуны истек
                    flag_doezd_l = False # флаг доезд налево ложь
                    povorot = False # флаг экстренного поворота ложь
            else: # иначе
                if max_y_left > 40: # если показание левого датчика больше 40
                    flag_doezd_l = False # флаг доезда налево ложь
                    povorot = False # флаг экстренного поворота ложь
            if direction == 1 and max_y_right == 0: # если направление по часовой стрелке и показание правого датчика = 0
                flag_doezd_l=False # флаг доезда налево ложь
                flag_doezd_r=True # флаг доезда направо истина
                povorot=True # флаг экстренного поворота истина
        else: # иначе
            timer_turn_l=time.time()  # обновляем таймер поворота налево

        if p > 55: # если ошибка больше 55
            p = 55 # ошибка равна 55
        if p < -55: # если ошибка меньше -55
            p = -55 # ошибка равна -55

        if -2 < p < 2: # если ошибка больше -2 и меньше 2
            p = 0 # ошибка равна 0

        if delta_banka!=0: # если обруливание знака не равно 0
            # если направление против часовой стрелки и флаг доезда налево истина и обруливание больше 0
            # или направление по часовой стрелки и флаг доезда направо истина и обруливание знака меньше 0
            if (direction==-1 and flag_doezd_l and delta_banka>0) or (direction==1 and flag_doezd_r and delta_banka<0):
                robot.serv(p) # поворачиваем сервомотор на ошибку
            else: # иначе
                robot.serv(delta_banka) # поворачиваем сервомотор на обруливание знака
        else: # иначе
             robot.serv(p) # поворачиваем сервомотор на ошибку

        robot.move(global_speed,0 , 100, wait=False) # включаем ведущий мотор с глобальной скоростью на 100 мс без задержки

        fps += 1 # прибавляем к счетчику fpa 1

        # выводим на экран текст с результатом подсчета fps
        cv2.putText(frame_show, "fps: " + str(fps_result), (520, 440), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (255, 255, 255), 2)

        if time.time() > fps_timer + 1: # если таймер на 1 секунду истек
            fps_result = fps # результат подсчета приравнивается к счетчику fps
            fps_timer = time.time() # обновление fps таймера
            fps = 0 # обнуление счетчика fps

        put_telemetry(frame_show) # вывод телеметрии