import cv2
import Rect
import Tracker

class Main:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.tracker = Tracker.Tracker(False)

        ##Initializes a Rectangle object from the Rect class, with a yellow color.
        self.rect1 = Rect.Rect((0,255,255), self.cap.read()[1])

    def main_loop(self):
        while True:
            cap, frame = self.cap.read()
            frame = cv2.flip(frame, flipCode=1)

            if self.tracker.drawing_rects:
                frame = self.tracker.get_movement(frame)
            else:
                areas = self.tracker.get_movement(frame)

            
            self.draw(frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def draw(self, frame):
        frame = self.draw_grid(frame)

        self.rect1.draw(frame) ##Draws the rectangle 1
        
        cv2.imshow("SuperNiceGame", frame)

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

            
            
