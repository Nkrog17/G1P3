import cv2
import numpy as np

class ColorTracker:

    ##The constructor.
    ##draw_rect is a boolean deciding whether or not contour rectangle is drawn
    ##trackedColor is an Integer deciding what Hue values to track.
    def __init__(self, draw_rect, trackedColor):
        self.drawing_rects = draw_rect ##A boolean deciding whether or not the contour will be shown
        self.sensitivity = 30 ##An integer deciding sensitivity (Higher sensitivity means a broader hue value is tracked)
        self.color = trackedColor ##The 3rd input in constructor will decide the color tracked. Should be in int between 0 and 180
        self.lower_saturation = 100 ##The lower boundary of saturation values tracked
        self.upper_saturation = 255##The upper boundary of saturations tracked
        self.lower_value = 100 ##The lower boundary of value tracked
        self.upper_value = 255##The upper boundary of value tracked.
        self.track_minimum_width = 10 ##The lowest width of the biggest contour for it to count.

    def get_movement(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) ##Converts the image to a HSV image.

        #Defining the range of color we want to track, in HSV
        lower_color = np.array([self.color - self.sensitivity, self.lower_saturation, self.lower_value])
        upper_color = np.array([self.color + self.sensitivity, self.upper_saturation, self.upper_value])
        

        # Threshold the HSV image to get only tracked colors
        # The mask creates a binary image where only the tracked color will be white and rest will be black
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Bitwise-AND mask and original image
        # Not quite sure what bitwise is or does, but it creates an image much like the mask where everything but the tracked color is black
        # The difference is that it shows the color instead of a black and white image.
        res = cv2.bitwise_and(frame, frame, mask = mask)


        #Creates the final frame where the color has been tracked
        final_frame = self.track_color(frame, mask)
        ##Returns this frame
        return  final_frame

    def track_color(self, frame, mask):
        ##Gets contours from mask (Since contours has to be found on a Binary image)
        ##The first input is the src image to take contours on. Second is contour retrieval mode. third is contour approximation.
        ##Contours are stored in a python list called contours.
        ##For more info on contours: https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html
        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        ##Creating an array the contain the area where the color is.
        areas = []
        
        ##If there are more than 0 contours find the biggest one and make a green rectangle around it.
        if len(contours) != 0:

            # draw in blue the contours that were found (All of them)
            cv2.drawContours(mask, contours, -1, 255, 3)
            
            #find the biggest contour area.
            c = max(contours, key = cv2.contourArea)
            # Sorts the contour list from smallest to biggest contour area.
            contours.sort(key = cv2.contourArea)


            ##Getting the rectangle attributes around the biggest contour (c)
            x,y,w,h = cv2.boundingRect(c)

            # Removes the biggest contour from the list
            contours.pop(len(contours)-1)

            # Inserts the biggest contour area into area array if it's width is bigger than min value.
            if w > self.track_minimum_width:
                ##Inserts the area with the most of the color (Biggest contour) into the areas array.
                areas.append(((x,y), (x+w, y+h)))

            # An if statement in which we find the second biggest contour and add it to area array
            if len(contours) != 0:
                # Finding the biggest contour (After biggest has been removed above, so technically 2nd biggest)
                c2 = max(contours, key = cv2.contourArea)
                # Finds the values of the rect surrounding it.
                x2, y2, w2, h2 = cv2.boundingRect(c2)
                
                if w2 > self.track_minimum_width:
                    # Adds the contour area to the area array
                    areas.append(((x2,y2), (x2+w2, y2+h2)))


            ##Only draws the rectangle behind biggest contour if drawing_rects is true.
            if self.drawing_rects and len(contours) != 0:
                # draw a rectangle around the biggest contour (in green)
                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0) ,2)
                ## Draws all small contours in blue
                cv2.drawContours(frame, contours, -1, 255, 3)
                #Draw a rectangle around the second biggest contour (in red)
                cv2.rectangle(frame, (x2,y2), (x2+w2, y2+h2), (0,0,255), 2)
        
        return areas
