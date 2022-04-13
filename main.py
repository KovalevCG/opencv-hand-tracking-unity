import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Variables
width, height = 1280, 720

# WebCam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Get the frame form Webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # flipVertical = cv2.flip(originalImage, 0)
    # Hands
    hands, img = detector.findHands(img)
    # Landmark Values
    data = []
    if hands:
        # Get first hand detected
        hand = hands[0]
        # Get the landmarks list
        lmList = hand['lmList']
        # print(lmList)
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])
        # print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

