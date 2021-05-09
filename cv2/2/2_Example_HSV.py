import simulatorAPI as uapi
import cv2
import numpy as np

class SimHSV:
    def __init__(self):
        self.HUE_MIN = 0
        self.HUE_MAX = 180
        self.SAT_MIN = 0
        self.SAT_MAX = 256
        self.VAL_MIN = 0
        self.VAL_MAX = 256
        self.trackbar_vals = {'min': np.array([self.HUE_MIN, self.SAT_MIN, self.VAL_MIN]),
                         'max': np.array([self.HUE_MAX, self.SAT_MAX, self.VAL_MAX])}
        cv2.namedWindow("HSV trackbars")
        # Создаем ползунки
        cv2.createTrackbar("Hue min", "HSV trackbars", self.HUE_MIN, self.HUE_MAX, self.make_setter('min', 0))
        cv2.createTrackbar("Hue max", "HSV trackbars", self.HUE_MAX, self.HUE_MAX, self.make_setter('max', 0))
        cv2.createTrackbar("Saturation min", "HSV trackbars", self.SAT_MIN, self.SAT_MAX, self.make_setter('min', 1))
        cv2.createTrackbar("Saturation max", "HSV trackbars", self.SAT_MAX, self.SAT_MAX, self.make_setter('max', 1))
        cv2.createTrackbar("Value min", "HSV trackbars", self.VAL_MIN, self.VAL_MAX, self.make_setter('min', 2))
        cv2.createTrackbar("Value max", "HSV trackbars", self.VAL_MAX, self.VAL_MAX, self.make_setter('max', 2))
    def make_setter(self, param_name, param_pos):
        def set_value(value):
            self.trackbar_vals[param_name][param_pos] = value
        return set_value

    def make_mask(self, frame):
        imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imageHSV, self.trackbar_vals['min'], self.trackbar_vals['max'])
        print(self.trackbar_vals['min'], self.trackbar_vals['max'])
        return mask



robot = uapi.UnityAPI().make_cv_robot("Robot")

hsv = SimHSV()

while True:

    #получаем кадр с робота
    frame = robot.camera.frame()

    #Выводим оригинальное изображение полученное с камеры робота
    cv2.imshow("fame", frame)

    # Выводим маску, полученную после обработки изображения
    mask = hsv.make_mask(frame)
    cv2.imshow("mask", mask)

    # Выводим фильтрованное изображение( для удобства отображения)
    cv2.imshow("Filtred image", cv2.bitwise_or(frame, frame, mask=mask))

    if cv2.waitKey(50) == 32:
        break

cv2.destroyAllWindows()