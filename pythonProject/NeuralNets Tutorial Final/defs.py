DISPLAY_W = 960
DISPLAY_H = 540
FPS = 30

DATA_FONT_SIZE = 18
DATA_FONT_COLOR = (40,40,40)
BG_FILENAME = '../BG.png'  #This is the positon of the background image
#If you are in a folder below with defs.py, the position is '../BG.png'

PIPE_FILENAME = '../Pipe.png'
PIPE_SPEED = 70/1000
PIPE_DONE = 1 #State number 1 means that the pipe is done moving
PIPE_MOVING = 0 #State number 0 means that the pipe is moving
PIPE_UPPER = 1 #State number 1 means that the pipe is at the top of the screen
PIPE_LOWER = 0 #State number 0 means that the pipe is at the bottom of the screen

PIPE_ADD_GAP = 160 #The gap between pairs of pipes
PIPE_MIN = 80 #How high the pipes may go (We are measuring distance from the top)
PIPE_MAX = 500 #How low the pipes may go
PIPE_START_X = DISPLAY_W #Pipes start on the right of the screen
PIPE_GAP_SIZE = 160 #Gap between two pipes in a pair (Where the bird can fly through)
PIPE_FIRST = 400 #The distance from the left of the screen to the first pipe pair

BIRD_FILENAME = '../Robin.png'
BIRD_START_SPEED = -0.32
BIRD_START_X = 200
BIRD_START_Y = 200
BIRD_ALIVE = 1
BIRD_DEAD = 0
GRAVITY = 0.001

GENERATION_SIZE = 60 #how many birds per generation

NNET_INPUTS = 2 #number of input nodes
NNET_HIDDEN = 5
NNET_OUTPUTS = 1

JUMP_CHANCE = 0.5 #flap when value higher or equal to 0.5

MAX_Y_DIFF = DISPLAY_H - PIPE_MIN - PIPE_GAP_SIZE/2 #Distance with Highest point for the bird, lowest for the pipe
MIN_Y_DIFF = PIPE_GAP_SIZE/2 - PIPE_MAX #Distance with Lowest point for the bird, highest for the pipe
Y_SHIFT = abs(MIN_Y_DIFF) #Absolute value of Min Y, which makes the distance
NORMALIZER = abs(MIN_Y_DIFF) + MAX_Y_DIFF #Maximum shift in distance

MUTATION_WEIGHT_MODIFY_CHANCE = 0.2
MUTATION_ARRAY_MIX_PERC = 0.5
MUTATION_CUT_OFF = 0.4
MUTATION_BAD_TO_KEEP = 0.2
MUTATION_MODIFY_CHANCE_LIMIT = 0.4