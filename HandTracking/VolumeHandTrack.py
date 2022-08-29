import cv2
import numpy as np
import time
import HandTrackingModule as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

hCam, wCam = 480, 640
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol, area = 0, 0
volBar, volPer = 400, 0
colorVol = (255, 204, 153)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findLandmarks(img)

    if len(lmList) != 0:
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        if 300 < area < 1000:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            
            volBar = np.interp(length, [25, 180], [400, 150])
            volPer = np.interp(length, [25, 180], [0, 100])
            
            smoothness = 5
            volPer = smoothness * round(volPer / smoothness)
            fingers = detector.fingersUp()

            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 204, 153)

            if length < 50:
                pass

    cv2.rectangle(img, (50, 150), (85, 400), colorVol, 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), colorVol, cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, colorVol, 2)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, colorVol, 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, colorVol, 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)