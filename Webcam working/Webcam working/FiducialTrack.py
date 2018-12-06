import copy
import cv2


class FiducialTrack:

    def __init__(self, draw_matches):
        self.drawing_matches = draw_matches
        self.fiducial = cv2.imread("fid4.png", 0)

        self.matches = 5
        self.thresh = 250

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

        #Get average coordinates.
        if list_kp2:
            xx, yy = zip(*list_kp2)
            avg_x = sum(xx)/len(xx)
            avg_y = sum(yy)/len(yy)

            temp_kp2 = copy.deepcopy(list_kp2)

            #Remove vertecies if they are too far away - possibly false positives.
            for vertex in temp_kp2:
                if vertex[0] > (avg_x + self.thresh) or vertex[0] < (avg_y - self.thresh):
                    list_kp2.remove(vertex)
                elif vertex[1] > (avg_y + self.thresh) or vertex[1] < (avg_y - self.thresh):
                    list_kp2.remove(vertex)

            #Update positions after vertecies are removed.
            if list_kp2:
                xx, yy = zip(*list_kp2)

                pos = ((int(min(xx)), int(min(yy))), (int(max(xx)), int(max(yy))))

                if self.drawing_matches:
                    cv2.rectangle(frame, pos[0], pos[1], (0,255,0), 3)

                    for vertex in list_kp2:
                        vertex = tuple((int(vertex[0]), int(vertex[1])))
                        cv2.rectangle(frame, vertex, vertex, (0,0,255), 5)

                return [pos]
            else:
                return []
        else:
            return []
        







        
