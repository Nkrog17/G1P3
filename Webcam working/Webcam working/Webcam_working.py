import copy
import cv2;
import numpy as np;
import random

##Frame resolution is 640(w)*480(h)
reference_Frame = None
activeSquareNr = 0
cap = cv2.VideoCapture(0)

class SquareScale:

    def __init__(self, x, y, s, b, c):

        self.x = x
        self.y = y
        self.s = s
        self.b = b
        self.c = c

    def scalingRect(self, frame):

        if self.s < width/6 and self.b < height/6:
            global activeSquareNr
            activeSquareNr = 1
            self.s += width * 0.001
            self.b += height * 0.001
            cv2.rectangle(frame, (int(self.x-self.s), int(self.y-self.b)), (int(self.x + self.s), int(self.y + self.b)), self.c)
        else:
            self.s = 0
            self.b = 0
            self.get_random_pos()
            
            
    def get_random_pos(self):
        rand = [1/6, 3/6, 5/6]
        raW = random.choice(rand)
        raH = random.choice(rand)

        check, frame = cap.read()
        height, width = frame.shape[:2]

        self.x = int(width*raW)
        self.y = int(height*raH)
    
#Ryd op her
rand = [1/6, 3/6, 5/6]
raW = random.choice(rand)
raH = random.choice(rand)

check, frame = cap.read()
height, width = frame.shape[:2]

myRect = SquareScale(int(width*raW), int(height*raH), 0, 0,(0, 255, 255, 0.5))


while True: 
    
    check, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if reference_Frame is None:
        reference_Frame = gray
        continue 

    frame_Difference = cv2.absdiff(reference_Frame, gray)
    threshold_Difference= cv2.threshold(frame_Difference,100,255,cv2.THRESH_BINARY)[1]
    threshold_Difference= cv2.dilate(threshold_Difference,None, iterations=0)

    (_,borders,_) = cv2.findContours(threshold_Difference.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in borders:
        if cv2.contourArea(contour) > 2000 and cv2.contourArea(contour) < 3000:
            continue

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    if activeSquareNr < 3:
        activeSquareNr += 1
        if activeSquareNr == 1:
            myRect.scalingRect(frame)

        activeSquareNr = 2

        if activeSquareNr == 2:
            myRect.scalingRect(frame)
    #Koden for at tegne et grid
    step_count = 3
    height = frame.shape[0]
    width =  frame.shape[1]
    lt = 1 # line thickness
    gridColor = (255,255,255)
    y_start = 0
    y_end = height
    step_sizey = int(width / step_count)
    step_sizex = int(height / step_count)

    for x in range(0, width, step_sizey ):
        #line = ((x, y_start), (x, y_end))
        cv2.line(frame,(x,y_start), (x, y_end),gridColor,lt)

        x_start = 0
        x_end = width

    for y in range(0, height, step_sizex):
            #line = ((x_start, y), (x_end, y))
            cv2.line(frame, (x_start, y), (x_end, y), gridColor, lt)

    cv2.imshow("frame",frame)

    if cv2.waitKey(1) & 0xFF == ord("w"):
        break


cv2.destroyAllWindows()


