import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

NAME = "Application name"

"""
The main loop of games 
"""
def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(NAME)

    while True:
        run_game(display_surf, fps_clock)

"""
Game loop, one game until game over
"""
def run_game(display_surf, fps_clock):
    # main game loop
    while True:  

        # Handle exit event, so that game can exit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
