import simulatorAPI as uapi
import cv2
import numpy as np

robot = uapi.UnityAPI().make_cv_robot("Robot")
manual_throttle = 50
flag_drill=False

robot.lamp.rgb(0, 0, 0)

# фильтр зеленого цвета
low = np.array([41, 92, 46])
up = np.array([ 61, 256, 256])

while True:
    frame = robot.camera.frame()

    # переводим изображение с камеры в формат HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # фильтруем по заданным параметрам
    mask = cv2.inRange(hsv, low, up)
    # на отфильтрованной маске выделяем контуры
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # перебераем все найденые контуры
    for contour in contours:
        #Создаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)
        #вычисляем площадь найденого контура
        area = cv2.contourArea(contour)
        if area > 5:
            #отрисовываем найденый контур
            cv2.drawContours(frame, contour, -1, (0, 0, 255), 2)
            # включаем зеленый свет
            robot.lamp.rgb(0,1,0)

    if len(contours)==0:
        # если нет найденых контуров, включаем красный свет
        robot.lamp.rgb(1,0,0)

    k = cv2.waitKey(1)
    #ручное управление
    # if k != -1: print(k)
    if k == 13:
        # клавиша  Enter включает/выключает бур
        flag_drill = not flag_drill

        robot.drill.power("on") if flag_drill else robot.drill.power("off")
        # предыдущая строчка равносильна закоментированному коду ниже
        # if flag_drill:
        #     robot.Drill.power("on")
        # else:
        #     robot.Drill.power("off")
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
        robot.brake(-100,-100)


    # выводим на изображение телеметрию робота
    # количество предметов в контейнере
    cv2.putText(frame, "Cargo: "+ str(len(robot.container.items()))+ " item", (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    # скорость робота
    cv2.putText(frame, "Speed: "+ str(round(robot.sensor.get_speed(),1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0), 1)
    cv2.imshow("Frame", frame)

