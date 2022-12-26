import cv2
import time
import os
import HandTrackingModule as htm
from cvzone.HandTrackingModule import HandDetector

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "images"
myList = os.listdir(folderPath)
# print(myList)
overlayList = []

for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    # print(f'{folderPath}/{imgPath}')
    overlayList.append(image)
# print(len(overlayList))
pTime = 0

detector = HandDetector(detectionCon=0.75, maxHands=1)
# detector1 = htm.handDetector(detectionCon=0.8)
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if len(hands) != 0:

        fingers = detector.fingersUp(hands[0])
        # print(fingers)

        noOfFingers = fingers.count(1)
        cv2.putText(img, f'{int(noOfFingers)} Fingers Up', (10, 400),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        if noOfFingers == 0:
            h, w, c = overlayList[noOfFingers].shape
            img[0:h, 0:w] = overlayList[noOfFingers]
        elif noOfFingers == 1:
            h, w, c = overlayList[noOfFingers].shape
            img[0:h, 0:w] = overlayList[noOfFingers]
        elif noOfFingers == 2:
            h, w, c = overlayList[noOfFingers].shape
            img[0:h, 0:w] = overlayList[noOfFingers]
        elif noOfFingers == 3:
            h, w, c = overlayList[noOfFingers].shape
            img[0:h, 0:w] = overlayList[noOfFingers]
        elif noOfFingers == 4:
            h, w, c = overlayList[noOfFingers].shape
            img[0:h, 0:w] = overlayList[noOfFingers]
        elif noOfFingers == 5:
            h, w, c = overlayList[noOfFingers].shape
            img[0:h, 0:w] = overlayList[noOfFingers]

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (450, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Hand Tracking!", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
