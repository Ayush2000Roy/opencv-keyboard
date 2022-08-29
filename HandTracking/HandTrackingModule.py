"""
MODULE: Hand Tracking Module
BY: Ayush Roy
DATE: 23-08-2022
"""

from operator import imod
import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode = False, maxHands = 2, modelComplexity = 1, detectionCon = 0.5, trackingCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findLandmarks(self, img, handNo = 0, draw = True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                ht, wid, ch = img.shape
                cx, cy = int(lm.x * wid), int(lm.y * ht)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
        
        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    def findDistance(self, p1, p2, img, draw = True):
        thumbX, thumbY = self.lmList[p1][1], self.lmList[p1][2]
        indexX, indexY = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (thumbX + indexX) // 2, (thumbY + indexY) // 2
        
        if draw:
            cv2.circle(img, (thumbX, thumbY), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (indexX, indexY), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (thumbX, thumbY), (indexX, indexY), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(indexX - thumbX, indexY - thumbY)
        return length, img, [thumbX, indexX, thumbY, indexY, cx, cy]

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        mirror_img = cv2.flip(img, 1)
        detector.findHands(mirror_img)
        lmList = detector.findLandmarks(mirror_img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(mirror_img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", mirror_img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()