import cv2
from cvzone.HandTrackingModule import HandDetector
import time


def NoOfFingers():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.70, maxHands=1)

    success, img = cap.read()
    hands, img = detector.findHands(img)
    vdo = cv2.imshow("Hand Gesture Mode", img)
    if len(hands) != 0:

        fingers = detector.fingersUp(hands[0])

        noOfFingers = fingers.count(1)
        print(noOfFingers)
        # print("From Function Called")
        return (noOfFingers, len(hands))
    return (0, 0)


# NoOfFingers()
