import cv2
import copy

class Tracker:

    def __init__(self):
        self.reference_frame = None
        self.timer = 0
        self.refresh_rate = 6
        self.low_thresh = 50
        self.high_thresh = 255

    def get_movement(self, frame):
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Opdaterer reference frame - experimental.
        if self.reference_frame is None:
            self.reference_frame = grayscale
        elif self.timer >= self.refresh_rate:
            self.reference_frame = grayscale

        if self.timer >= self.refresh_rate:
            self.timer = 0
        else:
            self.timer += 1

        #Eksperimenter med forksllig background subtractions
        frame_difference = cv2.absdiff(self.reference_frame, grayscale)
        threshold_difference = cv2.threshold(frame_difference, self.low_thresh, self.high_thresh,cv2.THRESH_BINARY)[1]
        threshold_difference = cv2.dilate(threshold_difference, None, iterations=0)

        final_frame = self.draw_borders(frame, threshold_difference)

        return final_frame

    def draw_borders(self, frame, threshold_difference):
        (_,borders,_) = cv2.findContours(threshold_difference.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in borders:
            if cv2.contourArea(contour) > 2000 and cv2.contourArea(contour) < 3000:
                continue

            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

        return frame
    
