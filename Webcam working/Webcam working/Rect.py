import cv2
import random

class Rect:

    def __init__(self, color, frame):
        self.height = 0 ##Used to store the height of the frame.
        self.width = 0 ##Width of the frame
        self.rand_pos(frame)
        self.s = 0 ##The scaling variable used to make the rectangles increase in size.
        self.c = color ##Color of the rectangle.
        self.ratio = 0 ##Will contain the ratio of the width and height (Width divided by Height)
        self.growth = 0 ##Will be used together with self.s (size) to define the growth of the rectangles.
        
    def draw(self, frame): ##Function to draw the rectangles on top of the frame.
        self.ratio = self.width / self.height ##Get the ratio of the frame
        self.growth = round(self.s * self.ratio) ##Used for the width to increase the same amount as the height percentage-wise
        if self.s < self.width/6 and self.s < self.height/6: ##If rectangle size is not bigger than the 9th of the frame it should be inside
            self.s += 1 ##Increases the size of the rectangle
            ##Draws the rectangle starting on self.x and y coordinates that keeps growing.
            cv2.rectangle(frame, (self.x - self.growth, self.y-self.s), (self.x + self.growth, self.y + self.s), self.c, 5)
        else:
            self.s = 0 ##Resets the size modifier
            self.rand_pos(frame) ##Chooses new random position for rectangle to spawn

    def rand_pos(self, frame):
        rand = [1/6, 3/6, 5/6] ##An array of values that will decide where the rectangle's start position is.
        raW = random.choice(rand) ##Chooses one random value from the array to be used as Width value.
        raH = random.choice(rand) ##Chooses one random value from the array to be used as Height value
        
        self.height, self.width = frame.shape[:2] ##Acquires the height and width of the frame

        self.x = int(self.width*raW) ##The x value the rect will spawn upon
        self.y = int(self.height*raH) ##The y value the rect will spawn upon
