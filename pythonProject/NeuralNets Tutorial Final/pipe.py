import pygame
import random
from defs import * #import properties from defs.py

class Pipe():
    def __init__(self, gameDisplay, x, y, pipe_type): #initialise all this stuff
        self.gameDisplay = gameDisplay
        self.state = PIPE_MOVING #Set status to pipe is moving
        self.pipe_type = pipe_type #Top or lower pipe?
        self.img = pygame.image.load(PIPE_FILENAME) #Look for the image of the pipe
        self.rect = self.img.get_rect() #Look the place of the image
        if pipe_type == PIPE_UPPER:
            y = y - self.rect.height #Use top of the pipe instead of bottom
        self.set_position(x,y) #Set position of the pipe

    def set_position(self, x, y): #Where the program puts the pipe initially
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy): #The pipes move left with a certain speed
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        if self.rect.right < 0: #If pipe has left the screen
            self.state = PIPE_DONE #change state of the pipe from moving to done

    def update(self, dt):
        if self.state == PIPE_MOVING: #When the pipes are moving
            self.move_position(-(PIPE_SPEED * dt), 0) #Define speed and call for move_position
            self.draw() #Draw pipe
            self.check_status() #Check if the pipe has left the screen


class PipeCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay #So you can use the display width and height
        self.pipes = [] #list of pipes

    def add_new_pipe_pair(self, x): #Add a new pair (UPPER and LOWER) of pipes
        top_y = random.randint(PIPE_MIN, PIPE_MAX - PIPE_GAP_SIZE) #Choose a random position between the boundaries and define the position for the upper pipe
        bottom_y = top_y + PIPE_GAP_SIZE #define position lower pipe

        p1 = Pipe(self.gameDisplay, x, top_y, PIPE_UPPER) #Tie the properties of the pipes together
        p2 = Pipe(self.gameDisplay, x, bottom_y, PIPE_LOWER)

        self.pipes.append(p1) #Create the new pipes
        self.pipes.append(p2)

    def create_new_set(self): #Only called in every new game
        self.pipes = [] #clear the pipe list
        placed = PIPE_FIRST

        while placed < DISPLAY_W: #As long as there is room left on the right
            self.add_new_pipe_pair(placed) #add new pipes
            placed += PIPE_ADD_GAP #and look for the position more to the right

    def update(self, dt):
        rightmost = 0

        for p in self.pipes: #for every pipe in the list
            p.update(dt)
            if p.pipe_type == PIPE_UPPER: #only look at the upper pipe
                if p.rect.left > rightmost: #look for the most right pipe
                    rightmost = p.rect.left #The position of the pipe is the left side of the image

        if rightmost < (DISPLAY_W - PIPE_ADD_GAP): #If the most right pair of pipes had enough room to its right
            self.add_new_pipe_pair(DISPLAY_W) #spawn new pipes

        self.pipes = [p for p in self.pipes if p.state == PIPE_MOVING] #remove pipe pairs that are not moving