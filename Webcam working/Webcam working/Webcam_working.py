import copy
import cv2;
import numpy as np;
import random

##Frame resolution is 640(w)*480(h)
reference_Frame = None
activeSquareNr = 0
cap = cv2.VideoCapture(0)

class SquareScale:

    def __init__(self, x, y, s, c):

        self.x = x
        self.y = y
        self.s = s
        self.c = c

    def scalingRect(self, frame):

        if self.s < width/6:
            global activeSquareNr
            activeSquareNr = 1
            self.s += 1
            cv2.rectangle(frame, (self.x-self.s, self.y-self.s), (self.x + self.s, self.y + self.s), self.c)
        else:
            self.s = 0
# def spawnNewRect():
rand = [1/6, 3/6, 5/6]
raW = random.choice(rand)
raH = random.choice(rand)

check, frame = cap.read()
height, width = frame.shape[:2]

myRect = SquareScale(int(width*raW), int(height*raH), 0, (0, 255, 255, 0.5))


while True: 
    
    check, frame = cap.read()

    cv2.line(frame, (0, 0), (int(frame.shape[1]), 0), (255, 255, 255), 1)
    cv2.line(frame, (0, frame.shape[0]), (0, 0), (255, 255, 255), 1)
    cv2.line(frame, (0,frame.shape[0] ), (frame.shape[1], frame.shape[0]), (255, 255, 255), 1)
    cv2.line(frame, (frame.shape[1], frame.shape[0]), (frame.shape[1], 0), (255, 255, 255), 1)
    cv2.line(frame, (int(frame.shape[1]*0.33), 0), (int(frame.shape[1]*0.33), frame.shape[0]), (255, 255, 255), 1)
    cv2.line(frame, (int(frame.shape[1] * 0.66), 0), (int(frame.shape[1] * 0.66), frame.shape[0]), (255, 255, 255), 1)
    cv2.line(frame, (0,int(frame.shape[0] * 0.33)), (frame.shape[1], int(frame.shape[0] * 0.33)), (255, 255, 255), 1)
    cv2.line(frame, (0, int(frame.shape[0] * 0.66)), (frame.shape[1], int(frame.shape[0] * 0.66)), (255, 255, 255), 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if reference_Frame is None:
        reference_Frame = gray
        continue 

    frame_Difference = cv2.absdiff(reference_Frame, gray)
    threshold_Difference= cv2.threshold(frame_Difference,30,255,cv2.THRESH_BINARY)[1]
    threshold_Difference= cv2.dilate(threshold_Difference,None, iterations=0)

    (_,borders,_) = cv2.findContours(threshold_Difference.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in borders:
        if cv2.contourArea(contour) > 3000 and cv2.contourArea(contour) < 5000:
            continue

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    print(activeSquareNr)
    if activeSquareNr < 3:
        activeSquareNr += 1
        if activeSquareNr == 1:
            myRect.scalingRect(frame)

        activeSquareNr = 2

        if activeSquareNr == 2:
            myRect.scalingRect(frame)

    cv2.imshow("frame",frame)

    if cv2.waitKey(1) & 0xFF == ord("w"):
        break

cv2.destroyAllWindows()


