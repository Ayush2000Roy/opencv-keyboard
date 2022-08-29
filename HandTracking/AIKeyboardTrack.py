import cv2
import HandTrackingModule as htm
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(trackingCon=0.8)
keyboard = Controller()
keysCap = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
        ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"]]
keys = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]]
finalText = ""

class Button():
    def __init__(self, position, btnText, size = [85, 85]):
        self.pos = position
        self.text = btnText
        self.size = size

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255, 255, 255), 4)

    return img

buttonListCap = []
for i in range(len(keysCap)):
    for j, key in enumerate(keysCap[i]):
        buttonListCap.append(Button([100 * j + 50, 100 * i + 50], key))
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findLandmarks(img)
    img = drawAll(img, buttonList)
    
    if len(lmList) != 0:
        fingers = detector.fingersUp()
        if not fingers[3]:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                
                if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 45:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)
        else:
            for button in buttonListCap:
                x, y = button.pos
                w, h = button.size
                
                if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 45:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2 , (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_SIMPLEX, 3 , (255, 255, 255), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)