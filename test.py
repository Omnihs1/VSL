import os
import cv2 as cv2
import numpy as np 
import math
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, minTrackCon=0.1):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.minTrackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True):
        img_bone = np.ones((img.shape[0], img.shape[1], 3)) * 255
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB)
        all_hands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(
                self.results.multi_handedness, self.results.multi_hand_landmarks
            ):
                # if handType == 'Right':
                myHand = {}
                # lmList
                mylmList = []
                xList = []
                yList = []
                zList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)
                    zList.append(pz)
                # bbox
                x_min, x_max = min(xList), max(xList)
                y_min, y_max = min(yList), max(yList)
                boxW, boxH = x_max - x_min, y_max - y_min
                bbox = x_min, y_min, boxW, boxH

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["xList"] = xList
                myHand["yList"] = yList
                myHand["zList"] = zList
                all_hands.append(myHand)
                # draw
                if draw:
                    self.mpDraw.draw_landmarks(
                        img_bone, handLms, self.mpHands.HAND_CONNECTIONS
                    )
        if draw:
            return all_hands, img_bone
        else:
            return all_hands
        
crop_x = 0
crop_y = 0
# crop_width = 1280*2/3
# crop_height = 720*2/3
video_path = 'cuong gui/Vietnamese_hand_sign-main/vietnamese_hand_sign/classes/Class A/A_4_20052023_3.mp4'
cap = cv2.VideoCapture(video_path)
frame_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(frame_total)
detector = HandDetector(maxHands=1)
offset = 40
img_size = 300
count = 0
while count < (frame_total - 10):
    ret, frame = cap.read()
    if frame is not None:
        crop_height = int(frame.shape[1]*2/3)
        crop_width = int(frame.shape[0]*2/3)
        cropped_frame = frame[crop_y: crop_y + crop_height, crop_x: crop_x + crop_width]
        # frame = cv2.resize(frame, (frame.shape[0] * 2, frame.shape[1] * 2))
        img = cropped_frame
        try:
            hands, img_bone = detector.findHands(img)
        except AttributeError:
            pass
        if hands:
            hand = hands[0]
            # output hand
            # print(hand["bbox"])
            x, y, w, h = hand["bbox"]
            # print(x, y, w, h)

            if h >= w:
                img_hand_crop = frame[
                    y - offset : y + h + offset, x - offset : x + h + offset
                ]
            else:
                img_hand_crop = frame[
                    y - offset : y + w + offset, x - offset : x + w + offset
                ]

            img_hand_resize = cv2.resize(
                img_hand_crop, [img_size, img_size]
            )
            count = 0
            print(count)
            cv2.imwrite("cuong gui/Vietnamese_hand_sign-main/kiemtra/" + f"{count}.jpeg" , img_hand_resize)
            count += 1
cap.release()
# print("done " + file_video)