import simulatorAPI as uapi
import cv2
import numpy as np

# подключиться и создать объект робот
robot = uapi.UnityAPI().make_drone_robot("Drone")

# используем класс для обнаружения QR меток
qrDecoder = cv2.QRCodeDetector()

while True:
    frame = robot.camera.frame()
    # демаем поиск меток на изображении с камеры
    retval, decoded_info, points, straight_qrcode = qrDecoder.detectAndDecodeMulti(frame )
    if points is not None:
        for i,pts in enumerate(points):
            # по умолчанию контур красный, метку видим но не можем расшифровать
            color_border = (0,0,255)
            if decoded_info[i]!="":
                # если есть названия метки, делаем зеленый контур
                color_border = (0, 255, 0)
                cv2.putText(frame, decoded_info[i], (int(pts[2][0]), int(pts[2][1] - 10)),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)


            x, y, w, h = cv2.boundingRect(pts)

            # Рисуем найденые координаты меткпи
            cv2.polylines(frame, np.int32([pts]), True, color_border,2)

    cv2.imshow("frame", frame)
    cv2.waitKey(1)
