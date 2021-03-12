import pygame
import random
from defs import *

class Bird():
    def __init__(self, gameDisplay): #initialize bird and its features
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE #Bird starts alive
        self.img = pygame.image.load(BIRD_FILENAME) #Load image of bird
        self.rect = self.img.get_rect() #Is used to find the position of bird
        self.speed = 0 #start with 0 speed
        self.time_lived = 0 #start with no time lived (This is for the AI to see if its doing well
        self.set_position(BIRD_START_X, BIRD_START_Y) #Startposition

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt): #When moving
        distance = 0 #empty distance
        new_speed = 0 #empty speed

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt) #s = ut + 0.5at^2
        new_speed = self.speed + (GRAVITY * dt) #v = u + at

        self.rect.centery += distance #Set the position of the bird on the y axis
        self.speed = new_speed #Set speed of the bird

        if self.rect.top < 0: #If the bird goes above the screen
            self.rect.top = 0 #stay in screen
            self.speed = 0 #set speed to 0

    def jump(self):
        self.speed = BIRD_START_SPEED #If jump is used, set speed again

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect) #Draw every frame

    def check_status(self, pipes): #Check if the bird still lives
        if self.rect.bottom > DISPLAY_H: #If it is below the screen
            self.state = BIRD_DEAD
        else: #if not
            self.check_hits(pipes) #check if it hit with the pipes

    def check_hits(self, pipes):
        for p in pipes: #for every pipe in the list
            if p.rect.colliderect(self.rect): #When the bird collides with a pipe
                self.state = BIRD_DEAD
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE: #if alive, call all the actions below
            self.time_lived += dt
            self.move(dt)
            self.draw()
            self.check_status(pipes)

class BirdCollection():
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipes):
        num_alive = 0
        for b in self.birds:
            if random.randint(0,4) == 1:
                b.jump()
            b.update(dt,pipes)
            if b.state == BIRD_ALIVE:
                num_alive += 1

        return num_alive
        