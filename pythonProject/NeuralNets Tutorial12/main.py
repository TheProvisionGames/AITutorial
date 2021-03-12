import pygame  # pygame has all kinds of interesting features, only some of them are used below
from defs import *  # import properties from defs.py
from pipe import PipeCollection  # Import pipe to use it here
from bird import BirdCollection


def update_label(data, title, font, x, y, gameDisplay):  # This is the format of the text on screen
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y


def update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive,
                       font):  # This is where you define the text that will get on screen
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000 / dt, 2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)  # show frames per second
    y_pos = update_label(round(game_time / 1000, 2), 'Game time', font, x_pos, y_pos + gap,
                         gameDisplay)  # show game time
    y_pos = update_label(num_iterations, 'Iterations', font, x_pos, y_pos + gap,
                         gameDisplay)  # show number of iterations
    y_pos = update_label(num_alive, 'Alive', font, x_pos, y_pos + gap,
                         gameDisplay)  # show number of iterations


def run_game():  # This plays when you start up main.py

    pygame.init()  # Initialize/open pygame
    gameDisplay = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))  # Set boundries for the game window
    pygame.display.set_caption('Learn to fly')  # Title of the game

    running = True  # Set running to true to use the running loop
    bgImg = pygame.image.load(BG_FILENAME)  # Load background image
    pipes = PipeCollection(gameDisplay)
    pipes.create_new_set()
    birds = BirdCollection(gameDisplay)

    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)  # Choose font and size

    clock = pygame.time.Clock()  # Pygame has a clock which can be used
    dt = 0  # delta time
    game_time = 0  # BeginTime = 0
    num_iterations = 1

    # From here the loop starts, all of the above will not play again
    while running:  # While the variable running is true

        dt = clock.tick(FPS)  # The difference in time takes the frames per second into account
        game_time += dt  # Add delta time to total time

        gameDisplay.blit(bgImg, (0, 0))  # Draw background image from the upper right corner

        for event in pygame.event.get():  # If something happens
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # When a key is pressed, put running to false, which stops the loop
                    running = False

        pipes.update(dt)  # update the drawn pipe
        num_alive = birds.update(dt, pipes.pipes)

        if num_alive == 0:  # every time the bird dies, create new game, but increase iterations
            pipes.create_new_set()
            game_time = 0
            birds.create_new_generation()
            num_iterations += 1

        update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, label_font)  # While running, update the text
        pygame.display.update()  # Draw all of what is called on top of the layers that are there (30 times per second, FPS)
        # This means that python only draws over the old images and does not delete them


if __name__ == "__main__":  # Calls the play function on opening
    run_game()
