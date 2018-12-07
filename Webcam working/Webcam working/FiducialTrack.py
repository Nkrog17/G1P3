import copy
import cv2


class FiducialTrack:

    def __init__(self, draw_matches):
        self.drawing_matches = draw_matches
        self.fiducial = cv2.imread("fid4.png", 0)

        self.matches = 4
        self.thresh = 50
        self.dot_width = 50

    def get_movement(self, frame):
        img1 = self.fiducial
        img2 = frame

        #ORB keypoint detector initialized.
        orb = cv2.ORB_create()

        kp1, des1 = orb.detectAndCompute(img1,None)
        kp2, des2 = orb.detectAndCompute(img2,None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        try:
            matches = bf.match(des1, des2)
            matches = sorted(matches, key = lambda x : x.distance)

            return self.track_fiducial(frame, matches[:self.matches], kp1, kp2)
        except:
            return []

    def track_fiducial(self, frame, matches, kp1, kp2):

        list_kp2 = []

        #Extract coordinates from matches.
        for mat in matches[:self.matches]:
            img2_idx = mat.trainIdx
            (x2, y2) = kp2[img2_idx].pt
            list_kp2.append([x2, y2])
        
##        #Get average coordinates.
##        if list_kp2:
##            xx, yy = zip(*list_kp2)
##            avg_x = sum(xx)/len(xx)
##            avg_y = sum(yy)/len(yy)
##
##            temp_kp2 = copy.deepcopy(list_kp2)
##
##
##            #Remove vertecies if they are too far away - possibly false positives.
##            for vertex in temp_kp2:
##                if vertex[0] > (avg_x + self.thresh) or vertex[0] < (avg_x - self.thresh):
##                    list_kp2.remove(vertex)
##                elif vertex[1] > (avg_y + self.thresh) or vertex[1] < (avg_y - self.thresh):
##                    list_kp2.remove(vertex)
##                    
##            
        #Update positions after vertecies are removed.
        pos = self.getContours(frame, list_kp2)
                
        if self.drawing_matches and list_kp2:
            for vertex in list_kp2:
                vertex = tuple((int(vertex[0]), int(vertex[1])))
                cv2.rectangle(frame, vertex, vertex, (255,0,0), self.dot_width)

                    
            return pos
        else:
            return []
    
    def getContours(self, frame, list_kp2):
        #Making a copy of frame to make rectangles and stuff on.
        im1 = copy.deepcopy(frame)
        
        #All matches are shown as blue dots
        for vertex in list_kp2:
            vertex = tuple((int(vertex[0]), int(vertex[1])))
            cv2.rectangle(im1, vertex, vertex, (255,0,0), self.dot_width)

        #DELETE THIS.
        cv2.imshow('Good stuff' , im1)
        
        #Creates mask (Binary image where only the blue dots (representing matches) is white and rest black.      
        mask = cv2.inRange(im1, (255,0,0), (255,0,0))
        

        #Gets contours from mask
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #Create an array to contain the areas where the matches are.
        areas = []

        if len(contours) != 0:
            # Draws contour (Inputs: src image, contours (as list), index contour (-1 shows ALL contours), and line thickness)
            cv2.drawContours(im1, contours, -1, (0,255,0), 3)

            #Find the biggest contour
            c = max(contours, key = cv2.contourArea)
            # Sorts the contour list from smallest to biggest contour area.
            contours.sort(key = cv2.contourArea)

            ##Getting the rectangle attributes around the biggest contour (c)
            x,y,w,h = cv2.boundingRect(c)

            # Removes the biggest contour from the list
            contours.pop(len(contours)-1)

            #Potentiall make an if statement that disregards contours smaller than x. (To avoid outliers to be counted)

            ##Inserts the area with the Biggest contour into the areas array.
            areas.append(((x,y), (x+w, y+h)))

            # An if statement in which we find the second biggest contour and add it to area array
            if len(contours) != 0:
                # Finding the biggest contour (After biggest has been removed above, so technically 2nd biggest)
                c2 = max(contours, key = cv2.contourArea)
                # Finds the values of the rect surrounding it.
                x2, y2, w2, h2 = cv2.boundingRect(c2)
                
                # Adds the contour area to the area array
                areas.append(((x2,y2), (x2+w2, y2+h2)))


            if self.drawing_matches and len(contours) != 0:
                # draw a rectangle around the biggest contour (in green)
                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0) ,2)
                ## Draws all small contours in blue
                cv2.drawContours(frame, contours, -1, (0,0,255) , 3)
                #Draw a rectangle around the second biggest contour (in red)
                cv2.rectangle(frame, (x2,y2), (x2+w2, y2+h2), (0,0,255), 2)

        #Shows mask
        cv2.imshow("test", mask)
        return areas
            

            





        
