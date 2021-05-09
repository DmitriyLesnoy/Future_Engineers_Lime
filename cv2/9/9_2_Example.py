import simulatorAPI as uapi
import cv2
import time
import numpy as np
import regulators

# подключиться и создать объект робот
robot = uapi.UnityAPI().make_drone_robot("Drone")
throttle = 100

state = 0
old_y_rotate=0


img1 = cv2.imread('H.png', 0)          # query Image

# orb = cv2.ORB_create(5000)
orb = cv2.ORB_create(nfeatures=10000, edgeThreshold=15, patchSize=31, nlevels=8, fastThreshold=20, scaleFactor=1.2,
                     WTA_K=2,
                     scoreType=cv2.ORB_FAST_SCORE, firstLevel=0)


# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)

while True:
    frame = robot.camera.frame()
    try:
        img2 = frame.copy()
        kp2, des2 = orb.detectAndCompute(img2, None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1, des2)

        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)

        good_matches = matches[:100]

        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

        dst = cv2.perspectiveTransform(pts, M)
        dst += (w, 0)  # adding offset

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)



        # Draw bounding box in Red
        # img3 = cv2.polylines(img3, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, **draw_params)
        x, y, w, h = cv2.boundingRect(np.int32(dst))

        if w/h >0.9 and w/h <1.1 and w>30:
            cv2.rectangle(img3, (x, y), (x + w, y + h), (255, 0, 0), 2)



        cv2.imshow("result", img3)
    except Exception as e:
        print(e)





    keys = robot.get_keys()
    # print(keys)
    if 49 in keys:

        state=0
    if 50 in keys:
        state=1
    if 51 in keys:
        img1 = frame.copy()

    if state==0:
        if 81 in keys:
           robot.gyro.add_torque_y(-100)
        if 69 in keys:
           robot.gyro.add_torque_y(100)
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
        if 32 in keys:
            robot.DroneController.up(100)

    cv2.imshow("frame", frame)
    cv2.waitKey(1)
