import simulatorAPI as uapi
import cv2
import time

# подключиться и создать объект робот
robot = uapi.UnityAPI().make_drone_robot("Drone")
throttle = 100


def drop(name):
    # выбрасываем из контейнера предмет по имени
    # перебираем все предметы в контейнере
    for item in robot.container.items():
        # если найден предмет с искомым именем
        if item['name'] == name:
            # даем коменду коннекторы выкинуть предмет
            robot.connector1.drop(item['id'])
            break


state = 0
state_names = ["Manual move", "State 1", "State 2", "State 3", "State 4"]
timer_stop = 0

while True:
    frame = robot.camera.frame()

    keys = robot.get_keys()
    # print(keys)
    # клавиши переключения состояний
    if 49 in keys:
        state = 0
    if 50 in keys:
        state = 1
        timer_stop = time.time()
    if 51 in keys:
        state = 2
        timer_stop = time.time()

    if state == 1:
        if time.time() > timer_stop + 2:
            state = 0
        cv2.putText(frame, "timer: " + str(round(time.time() - timer_stop, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

    if state == 2:
        if time.time() > timer_stop + 2:
            state = 0
        cv2.putText(frame, "timer: " + str(round(time.time() - timer_stop, 1)), (10, 60),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255), 2)

    if state == 0:
        if 51 in keys:
            print("Drop Ice")
            drop("Ice")
            robot.sleep(200)

        if 52 in keys:
            print("Drop Iron")
            drop("Iron")
            robot.sleep(200)

        if 53 in keys:
            print("Drop All")
            # даем команду выбросить все предметы их контейнера
            robot.connector1.drop_all()
            robot.sleep(200)

        if 87 in keys:
            robot.DroneController.forward(100)

        if 83 in keys:
            robot.DroneController.back(100)

        if 68 in keys:
            robot.DroneController.right(100)

        if 65 in keys:
            robot.DroneController.left(100)

        if 67 in keys:
            robot.DroneController.down(100)
            print("Heigh:", robot.sensor.get_position()['y'])
        if 32 in keys:
            robot.DroneController.up(100)
            print("Heigh:", robot.sensor.get_position()['y'])


    # вывод телеметрии на экран
    cv2.putText(frame, "State: " + state_names[state], (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)
    cv2.putText(frame, "Speed: " + str(round(robot.sensor.get_speed(), 1)), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
