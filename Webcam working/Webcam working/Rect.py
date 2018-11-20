import cv2
import random

class Rect:

    def __init__(self, frame):
        self.height = 0 ##Used to store the height of the frame.
        self.width = 0 ##Width of the frame
        self.rand_pos(frame)
        self.s = 0 ##The scaling variable used to make the rectangles increase in size.
        self.c = (0,0,0) ##Color of the rectangle.
        self.ratio = 0 ##Will contain the ratio of the width and height (Width divided by Height)
        self.growth = 0 ##Will be used together with self.s (size) to define the growth of the rectangles.
        self.pos1 = (0,0)
        self.pos2 = (0,0)
        self.touched = False

        self.timer = 0
        self.wait_time = 30

    def change_color(self):
        full = self.height/6
        if self.s <= full*0.4 and self.c != (255,0,0):
            self.c = (0,0,255)
        elif self.s <= full*0.8 and self.c != (255,255,0):
            self.c = (0,255,255)
        else:
            self.c = (0,255,0)
        
    def draw(self, frame): ##Function to draw the rectangles on top of the frame.
        if not self.touched:
            if self.timer >= self.wait_time:
                self.ratio = self.width / self.height ##Get the ratio of the frame
                self.growth = round(self.s * self.ratio) ##Used for the width to increase the same amount as the height percentage-wise

                self.pos1 = (self.x - self.growth, int(self.y-self.s))
                self.pos2 = (self.x + self.growth, int(self.y + self.s))
                self.s += 1.2 ##Increases the size of the rectangle
            else:
                self.pos1 = (self.x-4, self.y-4)
                self.pos2 = (self.x+4, self.y+4)
                self.timer += 1

            self.change_color()

            if self.s < self.width/6 and self.s < self.height/6: ##If rectangle size is not bigger than the 9th of the frame it should be inside
                ##Draws the rectangle starting on self.x and y coordinates that keeps growing.
                cv2.rectangle(frame, self.pos1, self.pos2, self.c, 5)
            else:
                self.s = 0 ##Resets the size modifier
                self.timer = 0
                self.rand_pos(frame) ##Chooses new random position for rectangle to spawn
        else:
            self.s = 0
            self.timer = 0
            self.rand_pos(frame)
            self.touched = False

    def rand_pos(self, frame):
        rand = [1/6, 3/6, 5/6] ##An array of values that will decide where the rectangle's start position is.
        raX = random.choice(rand) ##Chooses one random value from the array to be used as X value.
        if raX == 3/6:
            raY = 1/6
        else:
            raY = random.choice(rand) ##Chooses one random value from the array to be used as Y value
        
        self.height, self.width = frame.shape[:2] ##Acquires the height and width of the frame

        self.x = int(self.width*raX) ##The x value the rect will spawn upon
        self.y = int(self.height*raY) ##The y value the rect will spawn upon
