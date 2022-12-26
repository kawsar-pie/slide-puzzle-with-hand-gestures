
import cv2
import time
import os
from cvzone.HandTrackingModule import HandDetector

def NoOfFingers():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = HandDetector(detectionCon=0.75, maxHands=1)

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        if len(hands)!=0:
            break

    if len(hands)!=0:

        fingers = detector.fingersUp(hands[0])

        noOfFingers = fingers.count(1)
        # print(noOfFingers)
        return (noOfFingers,len(hands))
    cap.release()
    cv2.destroyAllWindows()

# print(NoOfFingers())
