import copy


import cv2;
import numpy as np;

reference_Frame = None

cap= cv2.VideoCapture(0)

while True: 
    
    check, frame= cap.read()

    
    gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_To_Gaussian= cv2.GaussianBlur(gray,(21,21),0)


    if reference_Frame is None:
        reference_Frame = gray
        continue 

    frame_Difference = cv2.absdiff(reference_Frame, gray)
    threshold_Difference= cv2.threshold(frame_Difference,30,255,cv2.THRESH_BINARY)[1]
    threshold_Difference= cv2.dilate(threshold_Difference,None, iterations=0)

    (_,borders,_) = cv2.findContours(threshold_Difference.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in borders:
        if cv2.contourArea(contour) <5000:
            continue

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)


       


    cv2.imshow("frame",frame)
    

    
  

    if cv2.waitKey(1) & 0xFF == ord("w"):
        break

cv2.destroyAllWindows()


