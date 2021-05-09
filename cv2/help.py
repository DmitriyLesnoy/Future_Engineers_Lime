#пустая матрица
#акфьу = np.ones((640,480,3), dtype=np.uint8)

#Изменить размер матрицы
#frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
#frame = cv2.resize(frame, (640,480), interpolation=cv2.INTER_CUBIC)
#frame = cv2.resize(frame, (640,480))

# размеры матрицы
#y = frame.shape[0]
#x = frame.shape[1]
#y,x,z  = frame.shape

# вырезать часть кадра(кроп)
# frame = frame[d.top(): d.bottom(), d.left():d.right()].copy()
# frame = frame[100: 300, 0:x].copy()

# вырезать часть изображение, снизу полоска 150 по Y, по X вся ширина
#frame = frame[frame.shape[0] - 150: frame.shape[0], 0: frame.shape[1]].copy()

#конвертировать в черно-белый формат
#gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# вывести на экран текст
#cv2.putText(frame, str("test"), (100, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

# robot.text_to_frame(frame, "hello", 20, 20)

# обьеденить две матрицы по горизонтале
#np.vstack([frame1, frame2])

# обьеденить две матрицы по вертикале
#np.hstack([frame1, frame2])

# найти контуры
#    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# отрисовать контуры
#cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

# создать контур и вычислить его площадь
#countur_rect = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
#k = cv2.contourArea(countur_rect)

# найти rect вокруг контура
#x, y, w, h = cv2.boundingRect(contur)

#отрисовать прямоугольник
#cv2.rectangle(framel, (x, y), (x + w, y + h), (255, 0, 0), 2)

# круг
#cv2.circle(frame, (x, y), z, (0, 255, 0), 2)

# расстояние между двумя точками numpy
# def dist(xa,ya,xb,yb,za=0,zb=0):
#     return np.sqrt(np.sum((np.array((xa, ya, za))-np.array((xb, yb, zb)))**2))
# пример работы функции
#p1 = distance_between_points(pos[0][0], pos[0][1], pos[1][0], pos[1][1])

# HSV
# low = np.array([80, 0, 0])
# up = np.array([100, 255, 255])
# frame1 = frame[420: 480, 100:540]
# hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
# mask1 = cv2.inRange(hsv1, low, up)
# im2, contours1, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


#  перезагрузка
# import os
# os.system('sudo shutdown -r now')

#присвоение с сравнением одной строчкой
#n = "1" if mode == 'train' else "0"

# вырезать изображение по маске
#fg = cv2.bitwise_or(img, img, mask=mask)

# инвертировать маску
#mask = cv2.bitwise_not(mask)

#создать пустой массив
#empty_img = np.zeros_like(img)

# создать маску и отвильтровать пиксели
#mask = np.zeros_like(filteredImg, dtype='uint8')
# mask[(filteredImg > 100) & (filteredImg < 130) ] = 255

#интерполировать значения на диапазон . аналог map arduino
#np.interp(joy_y1, [-1, 1], [-255, 255])

#обрезать по краям. аналог constrain
#np.clip(value, 0, 255)


# распечатать ошибку исключения
# try:
#     #код
# except Exception as e:
#     print(e)

#создать пустой кадр по подобию образца
# frame_mask = np.zeros_like(frame)

#функция генерации случайных чисел в диапазоне numpy
#numpy.random.randint(100, 1000)
#парисовать линию
#cv2.line(frame_show, (int(X1), int(Y1)), (int(X2), int(Y2)), (0, 255, 0), 3)

# def distance_between_points(self, x1, y1, x2, y2):
#     return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# def map(self, x, in_min, in_max, out_min, out_max):
#     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# def constrain(self, x, out_min, out_max):
#     if x < out_min:
#         return out_min
#     elif out_max < x:
#         return out_max
#     else:
#         return x

# import threading
# my_thread_mouse = threading.Thread(target=mouse_move)
# my_thread_mouse.daemon = True
# my_thread_mouse.start()






