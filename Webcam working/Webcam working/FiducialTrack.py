import copy
import cv2


class FiducialTrack:

    def __init__(self, draw_matches, fiducial, color):
        self.drawing_matches = draw_matches
        self.fiducial = cv2.imread(fiducial, 0)
        self.color = color

        self.matches = 40
        self.dot_width = 30

    def get_movement(self, frame):
        img1 = self.fiducial
        img2 = frame

        #ORB keypoint detector initialized.
        orb = cv2.ORB_create()

        #Find feature keypoints on both fiducial and webcam frame.
        kp1, des1 = orb.detectAndCompute(img1,None)
        kp2, des2 = orb.detectAndCompute(img2,None)

        #Unknown values...
        index_params = dict(algorithm = 6,
                   table_number = 6,
                   key_size = 12,
                   multi_probe_level = 1)
        search_params = dict(checks=50)

        #Flann is a mathcer - it compares keypoints and assess whether or not they are matches.
        flann = cv2.FlannBasedMatcher(index_params,search_params)

        try:
            #Create matches with Flann and sort them after quality. (distance)
            matches = flann.knnMatch(des1,des2,k=2)
            matches = sorted(matches, key = lambda x : x[1].distance)

            #Give 40 matches to track_fiducial 
            return self.track_fiducial(frame, matches[:self.matches], kp1, kp2)
        except:
            return []

    def track_fiducial(self, frame, matches, kp1, kp2):

        list_kp2 = []

        #Extract coordinates from matches.
        for mat in matches[:self.matches]:
            img2_idx = mat[1].trainIdx
            (x2, y2) = kp2[img2_idx].pt
            list_kp2.append([x2, y2])
 
        #Update positions after vertecies are removed.
        pos = self.getContours(frame, list_kp2)
                
        if self.drawing_matches and list_kp2:
            for vertex in list_kp2:
                vertex = tuple((int(vertex[0]), int(vertex[1])))
                cv2.rectangle(frame, vertex, vertex, (255,0,0), self.dot_width)
                
        return pos
    
    def getContours(self, frame, list_kp2):
        #Making a copy of frame to make rectangles and stuff on.
        im1 = copy.deepcopy(frame)
        
        #All matches are shown as blue dots
        for vertex in list_kp2:
            vertex = tuple((int(vertex[0]), int(vertex[1])))
            cv2.rectangle(im1, vertex, vertex, (255,0,0), self.dot_width)
        
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


            if self.drawing_matches and len(contours) != 0:
                # draw a rectangle around the biggest contour (in green)
                cv2.rectangle(frame, (x,y), (x+w, y+h),self.color ,2)
                ## Draws all small contours in blue
               # cv2.drawContours(frame, contours, -1, (0,0,255) , 3)

        #Shows mask
        if self.drawing_matches:
            cv2.imshow("test", mask)
            cv2.imshow('Good stuff' , im1)
            
        return areas
            

            





        
