import pygame
import random
from defs import *
from nnet import Nnet
import numpy as np

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

    def create_offspring(p1, p2, gameDisplay): #from two other birds, one new bird can be created based on their neural net weights
        new_bird = Bird(gameDisplay)
        new_bird.nnet.create_mixed_weights(p1.nnet, p2.nnet)
        return new_bird


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
        for b in self.birds: #for every bird
            b.fitness += b.time_lived * PIPE_SPEED #fitness determined by time lived and the distance to the gap of the pipes

        self.birds.sort(key=lambda x: x.fitness, reverse=True) #sort birds by fitness

        cut_off = int(len(self.birds) * MUTATION_CUT_OFF)
        good_birds = self.birds[0:cut_off] #The good birds are the top performing birds
        bad_birds = self.birds[cut_off:] #The rest are bad birds
        num_bad_to_take = int(len(self.birds) * MUTATION_BAD_TO_KEEP) #some of the bad birds should be kept

        for b in bad_birds: #for every bad bird
            b.nnet.modify_weight() #modify neural net weights

        new_birds = [] #make a list of new birds that are needed for every deleted bad bird

        idx_bad_to_take = np.random.choice(np.arange(len(bad_birds)), num_bad_to_take, replace=False) #Choose which birds to take to the next round

        for index in idx_bad_to_take:
            new_birds.append(bad_birds[index])

        new_birds.extend(good_birds)

        while len(new_birds) < len(self.birds): #when more birds are needed
            idx_to_breed = np.random.choice(np.arange(len(good_birds)), 2, replace=False) #pick random parents from the good birds
            if idx_to_breed[0] != idx_to_breed[1]: #make sure the parent birds aren't the same
                new_bird = Bird.create_offspring(good_birds[idx_to_breed[0]], good_birds[idx_to_breed[1]], self.gameDisplay) #Breed from the two chosen birds together
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT: #There is a chance that the weights of the neural net are changed
                    new_bird.nnet.modify_weight()
                new_birds.append(new_bird)

        for b in new_birds:
            b.reset();

        self.birds = new_birds