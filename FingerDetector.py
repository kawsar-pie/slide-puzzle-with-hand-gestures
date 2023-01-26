import cv2
from cvzone.HandTrackingModule import HandDetector

def NoOfFingers():
    wCam, hCam = 1200, 780
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = HandDetector(detectionCon=0.70, maxHands=1)

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        if len(hands)!=0:
            break

    if len(hands)!=0:

        fingers = detector.fingersUp(hands[0])

        noOfFingers = fingers.count(1)
        # print(noOfFingers)
        # print("From Function Called")
        return (noOfFingers,len(hands))

    cap.release()
    cv2.destroyAllWindows()
    


