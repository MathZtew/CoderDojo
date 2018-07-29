import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

NAME = "Tetris"


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(NAME)

    while True:
        run_game(display_surf, fps_clock)


def run_game(display_surf, fps_clock):
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        display_surf.fill(BLACK)
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()