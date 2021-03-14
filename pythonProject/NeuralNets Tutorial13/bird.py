import pygame
import random
from defs import *
from nnet import Nnet

class Bird():
    def __init__(self, gameDisplay): #initialize bird and its features
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE #Bird starts alive
        self.img = pygame.image.load(BIRD_FILENAME) #Load image of bird
        self.rect = self.img.get_rect() #Is used to find the position of bird
        self.speed = 0 #start with 0 speed
        self.fitness = 0
        self.time_lived = 0 #start with no time lived (This is for the AI to see if its doing well
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS) #Initialize different nodes with nnet
        self.set_position(BIRD_START_X, BIRD_START_Y) #Startposition

    def reset(self): #Reset all changed values
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

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

    def jump(self, pipes):
        inputs = self.get_inputs(pipes)
        val = self.nnet.get_max_value(inputs)
        if val > JUMP_CHANCE:
            self.speed = BIRD_START_SPEED #If jump is used, set speed again

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect) #Draw every frame

    def check_status(self, pipes): #Check if the bird still lives
        if self.rect.bottom > DISPLAY_H: #If it is below the screen
            self.state = BIRD_DEAD
        else: #if not
            self.check_hits(pipes) #check if it hit with the pipes

    def assign_collision_fitness(self, p): #Set fitness value to how close it was to the pipe when it died
        gap_y = 0
        if p.pipe_type == PIPE_UPPER: #If collided into upper pipe
            gap_y = p.rect.bottom + PIPE_GAP_SIZE/2 #Distance to gap from upper pipe
        else:
            gap_y = p.rect.top - PIPE_GAP_SIZE/2 #Distance to gap from bottom pipe

        self.fitness = -(abs(self.rect.centery - gap_y))

    def check_hits(self, pipes):
        for p in pipes: #for every pipe in the list
            if p.rect.colliderect(self.rect): #When the bird collides with a pipe
                self.state = BIRD_DEAD
                self.assign_collision_fitness(p)
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE: #if alive, call all the actions below
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes)

    def get_inputs(self, pipes):
        closest = DISPLAY_W * 2
        bottom_y = 0
        for p in pipes: #Which pipe is closest?
            if p.pipe_type == PIPE_UPPER and p.rect.right < closest and p.rect.right > self.rect.left:
                closest = p.rect.right
                bottom_y = p.rect.bottom

        horizontal_distance = closest - self.rect.centerx #how far the closest pipe is horizontally
        vertical_distance = (self.rect.centery) - (bottom_y + PIPE_GAP_SIZE / 2) #and vertically

        inputs = [
            ((horizontal_distance / DISPLAY_W) * 0.99) + 0.01,
            (((vertical_distance + Y_SHIFT) / NORMALIZER) * 0.99) + 0.01
        ]

        return inputs


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
            b.update(dt,pipes)
            if b.state == BIRD_ALIVE:
                num_alive += 1

        return num_alive

    def evolve_population(self):
        for b in self.birds:
            b.fitness += b.time_lived * PIPE_SPEED

        self.birds.sort(key=lambda x: x.fitness, reverse=True)

        for b in self.birds:
            print('fitness:', b.fitness)

        self.create_new_generation()
        