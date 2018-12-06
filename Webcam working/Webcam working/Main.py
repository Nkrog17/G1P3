import cv2
import Rect
import Tracker
import ColourTrack
import FiducialTrack

class Main:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        ##Tracker for pixel change
        ##self.tracker = Tracker.Tracker(False)

        ##Tracker for ColorTracking
        ##self.tracker = ColourTrack.ColorTracker(False, 60)

        ##Tracker for fiducials
        self.tracker = FiducialTrack.FiducialTrack(True)
        
        self.score = 0

        ##Initializes a list of Rectangle objects from the Rect class.
        self.rects = [Rect.Rect(self.cap.read()[1]), Rect.Rect(self.cap.read()[1])]

        self.play_time = 0

    def main_loop(self):
        while True:
            cap, frame = self.cap.read()
            frame = cv2.flip(frame, flipCode=1)

            areas = self.tracker.get_movement(frame)

            self.check_collision(frame, areas)
            
            self.draw(frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def check_collision(self, frame, areas):
        for rect in self.rects:
            if rect.timer < rect.wait_time:
                continue
            if not rect.touched:
                #Loop through untouched rects on screen
                p1,p2 = rect.pos1, rect.pos2
                for area in areas:
                    #Loop through activated areas from tracking.
                    p3, p4 = area[0], area[1]
                    #Check if the areas intersect with the rect and give points.
                    if not (p2[1] < p3[1] or p1[1] > p4[1] or p2[0] < p3[0] or p1[0] > p4[0]):
                        self.award_points(rect, frame)

    def award_points(self, rect, frame):
        if not rect.touched:
            if rect.c == (0,0,255):
                score = -1
            elif rect.c == (0,255,255):
                score = 1
            else:
                score = 2
            rect.score = score
            rect.point_timer = 0
            rect.point_pos = (int(frame.shape[1]*rect.dX-20),int(frame.shape[0]*rect.dY+10))
            rect.point_color = rect.c
            self.score += score
            rect.touched = True
            rect.allowed_to_grow = False
            self.play_time += 1

    def draw_points(self, frame, rect):
        if rect.point_timer < 40:
            cv2.putText(frame, str(rect.score), rect.point_pos,
                        cv2.FONT_HERSHEY_TRIPLEX, 2, rect.point_color)
            rect.point_timer += 1

    def sync_rects(self):
        allowed = [x.allowed_to_grow for x in self.rects]
        if True not in allowed:
            for rect in self.rects:
                rect.allowed_to_grow = True

    def draw(self, frame):
        frame = self.draw_grid(frame)
        frame = self.draw_score(frame)

        self.sync_rects()

        for rect in self.rects:
            self.draw_points(frame, rect)
            other_rects = list(self.rects)
            other_rects.remove(rect)
            rect.draw(frame, other_rects) ##Draws the rectangles
        
        cv2.imshow("SuperNiceGame", frame)

    def draw_score(self, frame):
        cv2.putText(frame, str(self.score), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

        return frame

    def draw_grid(self, frame):
        divisions = 3
        lt = 1
        color = (255,255,255)

        step_x = int(frame.shape[1] / divisions)
        step_y = int(frame.shape[0] / divisions)
        
        for i in range(1, divisions):
            cv2.line(frame, (i*step_x, 0), (i*step_x, frame.shape[0]), color, lt)
            cv2.line(frame, (0, i*step_y), (frame.shape[1], i*step_y), color, lt)

        return frame

        
controller = Main()
controller.main_loop()

            
            
