import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60  # Frames per second 

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# The name of the application
NAME = "Application name"

def main():
    """
    The main loop of games 
    """
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(NAME)

    while True:
        run_game(display_surf, fps_clock)


def run_game(display_surf, fps_clock):
    """
    Game loop, one game until game over
    """
    # main game loop
    while True:
        display_surf.fill(BLACK)

        # Handle exit event, so that game can exit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        ###################################################
        # Your game code goes here
        ###################################################

        # This should be on the end of the loop
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
                
