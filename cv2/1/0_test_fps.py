import simulatorAPI as uapi
import time
import cv2

robot = uapi.UnityAPI().make_cv_robot("Robot")

manual_throttle = 50

robot.lamp.rgb(0, 0, 1)
fps_count=0
fps=0
timer_fps= time.time()+1
while True:
    frame = robot.camera.frame()
    if robot.camera.flag_new_frame:
        fps_count+=1
    if time.time()>timer_fps:
        timer_fps=time.time()+1
        fps = fps_count
        print(fps)
        fps_count =0

    cv2.putText(frame, "fps: " + str(fps), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)

    keys = robot.get_keys()

    if 87 in keys:
        robot.move(50,50,500)
        robot.lamp.rgb(0, 0, 1)
        # robot.sleep(100)
    if 83 in keys:
        robot.move(-50, -50, 500)
        # robot.sleep(500)
    if 65 in keys:
        robot.move(-50, 50)

    if 68 in keys:
        robot.move(50, -50)
    if 32 in keys:
        robot.lamp.rgb(1, 1, 1)
        print(robot.sensor.get_position())

