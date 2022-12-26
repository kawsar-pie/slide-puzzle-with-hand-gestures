import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=3, detectionCon=0.75)
video = cv2.VideoCapture(0)

while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hand,img = detector.findHands(img)
    fing = cv2.imread("images/0.jpg")
    if hand:
        lmlist = hand[0]
        if lmlist:
            fingerup = detector.fingersUp(lmlist)
            if fingerup == [0, 1, 0, 0, 0]:
                fing = cv2.imread("images/1.jpg")
            if fingerup == [0, 1, 1, 0, 0]:
                fing = cv2.imread("images/2.jpg")
            if fingerup == [0, 1, 1, 1, 0]:
                fing = cv2.imread("images/3.jpg")
            if fingerup == [0, 1, 1, 1, 1]:
                fing = cv2.imread("images/4.jpg")
            if fingerup == [1, 1, 1, 1, 1]:
                fing = cv2.imread("images/5.jpg")
    h, w, c = fing.shape
    fing = cv2.resize(fing, (h, w))
    img[0:w, 0:h] = fing
    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
