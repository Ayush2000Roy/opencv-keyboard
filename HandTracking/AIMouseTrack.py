"""
<!-- DISCONTINUED -->
ERROR: 'AUTOPY' LIBRARY
INFO: 'AUTOPY' LIBRARY COULDN'T BE INSTALLED IN PYTHON 3.10.x AND FURTHER INSTALLATION IN PYTHON 3.8 &
        LOWER NOT POSSIBLE DUE TO UNRESOLVABLE ERROR OF 'LEGACY-INSTALL-FAILURE'
DATE: 23-08-2022
"""
import cv2
import numpy as np
import time
import HandTrackingModule as htm

hCam, wCam = 480, 640
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
colorVol = (255, 204, 153)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findLandmarks(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # index finger
        x2, y2 = lmList[12][1:] # middle finger
        
        fingers = detector.fingersUp()
        print(fingers)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, colorVol, 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)