import cv2
import random

activeSquareNr = 0

class Controller:

    def __init__(self):
        self.reference_Frame = None
        self.cap = cv2.VideoCapture(0)
        self.myRect = Rect((0,255,255), self.cap.read()[1]) #dette er midlertidigt.

    def main_loop(self):
        global activeSquareNr
        while True: #Ryk så meget kode ud i funktioner som muligt, så vores mail loop ikke er for langt.
            
            check, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.reference_Frame is None:
                self.reference_Frame = gray

            frame_Difference = cv2.absdiff(self.reference_Frame, gray)
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
                    self.myRect.draw(frame)

                activeSquareNr = 2

                if activeSquareNr == 2:
                    self.myRect.draw(frame) #Hav evt en liste af rects, så vi kan have flere end en. 

            #Lav en funktion, som tegner vores grid - og brug evt loop i stedet for.

            cv2.line(frame, (0, 0), (int(frame.shape[1]), 0), (255, 255, 255), 1)
            cv2.line(frame, (0, frame.shape[0]), (0, 0), (255, 255, 255), 1)
            cv2.line(frame, (0,frame.shape[0] ), (frame.shape[1], frame.shape[0]), (255, 255, 255), 1)
            cv2.line(frame, (frame.shape[1], frame.shape[0]), (frame.shape[1], 0), (255, 255, 255), 1)
            cv2.line(frame, (int(frame.shape[1]*0.33), 0), (int(frame.shape[1]*0.33), frame.shape[0]), (255, 255, 255), 1)
            cv2.line(frame, (int(frame.shape[1] * 0.66), 0), (int(frame.shape[1] * 0.66), frame.shape[0]), (255, 255, 255), 1)
            cv2.line(frame, (0,int(frame.shape[0] * 0.33)), (frame.shape[1], int(frame.shape[0] * 0.33)), (255, 255, 255), 1)
            cv2.line(frame, (0, int(frame.shape[0] * 0.66)), (frame.shape[1], int(frame.shape[0] * 0.66)), (255, 255, 255), 1)

            cv2.imshow("frame",frame)

            if cv2.waitKey(1) & 0xFF == ord("w"):
                break


class Rect:

    def __init__(self, color, frame):
        self.height = 0
        self.width = 0
        self.rand_pos(frame)
        self.s = 0
        self.c = color

    def draw(self, frame):
        if self.s < self.width/6:
            global activeSquareNr #Undgå globale variabler. Gør det evt til en variabel hos Controller.
            activeSquareNr = 1
            self.s += 1
            cv2.rectangle(frame, (self.x-self.s, self.y-self.s), (self.x + self.s, self.y + self.s), self.c, 5)
        else:
            self.s = 0
            self.rand_pos(frame)

    def rand_pos(self, frame):
        rand = [1/6, 3/6, 5/6]
        raW = random.choice(rand)
        raH = random.choice(rand)
        
        self.height, self.width = frame.shape[:2]

        self.x = int(self.width*raW)
        self.y = int(self.height*raH)

#Denne funktion vil blive kørt - den starter og slutter programmet.
def run():
    game = Controller()
    game.main_loop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()






