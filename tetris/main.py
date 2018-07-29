import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60

VERTICAL_BLOCKS = 4
HORIZONTAL_BLOCKS = 4

assert WINDOW_HEIGHT % VERTICAL_BLOCKS == 0
assert WINDOW_WIDTH % HORIZONTAL_BLOCKS == 0

CELL_WIDTH = int(WINDOW_WIDTH / HORIZONTAL_BLOCKS)
CELL_HEIGHT = int(WINDOW_HEIGHT / VERTICAL_BLOCKS)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)  # I
BLUE = (0, 0, 255)  # J
ORANGE = (255, 165, 0)  # L
YELLOW = (255, 255, 0)  # 0
GREEN = (0, 255, 0)  # S
PURPLE = (128, 0, 128)  # T
RED = (255, 0, 0)  # Z

I = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, BLACK, BLACK, BLACK],
     [CYAN, CYAN, CYAN, CYAN],
     [BLACK, BLACK, BLACK, BLACK]]
J = [[BLACK, BLACK, BLACK, BLACK],
     [BLUE, BLACK, BLACK, BLACK],
     [BLUE, BLUE, BLUE, BLACK],
     [BLACK, BLACK, BLACK, BLACK]]
L = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, BLACK, BLACK, ORANGE],
     [BLACK, ORANGE, ORANGE, ORANGE],
     [BLACK, BLACK, BLACK, BLACK]]
O = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, YELLOW, YELLOW, BLACK],
     [BLACK, YELLOW, YELLOW, BLACK],
     [BLACK, BLACK, BLACK, BLACK]]
S = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, BLACK, BLACK, BLACK],
     [BLACK, GREEN, GREEN, BLACK],
     [GREEN, GREEN, BLACK, BLACK]]
T = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, BLACK, BLACK, BLACK],
     [BLACK, BLACK, PURPLE, BLACK],
     [BLACK, PURPLE, PURPLE, PURPLE]]
Z = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, BLACK, BLACK, BLACK],
     [BLACK, RED, RED, BLACK],
     [BLACK, BLACK, RED, RED]]

NAME = "Tetris"


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(NAME)

    while True:
        run_game(display_surf, fps_clock)


def run_game(display_surf, fps_clock):
    #board = [[BLACK for a in range(VERTICAL_BLOCKS)] for b in range(HORIZONTAL_BLOCKS)]
    board = Z
    keys = {'up': False}
    while True:  # main game loop
        display_surf.fill(BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    keys['up'] = True
                    board = rotate_block(board)
            if event.type == KEYUP:
                if event.key == K_UP:
                    keys['up'] = False

        draw_game(display_surf, board)

        # Last thing to be done
        fps_clock.tick(FPS)


def draw_game(display_surf, board):
    """ Draws the game """
    draw_board(display_surf, board)
    draw_grid(display_surf)
    pygame.display.update()


def draw_grid(display_surf):
    """ Draws the supporting grid on the game board. """
    for x in range(0, WINDOW_WIDTH, CELL_WIDTH):  # draw vertical lines
        pygame.draw.line(display_surf, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_HEIGHT):  # draw horizontal lines
        pygame.draw.line(display_surf, WHITE, (0, y), (WINDOW_WIDTH, y))


def draw_board(display_surf, board):
    """Draws the whole game board, where the board is an array of colours """
    assert len(board) == VERTICAL_BLOCKS
    assert len(board[0]) == HORIZONTAL_BLOCKS

    for x in range(VERTICAL_BLOCKS):
        for y in range(HORIZONTAL_BLOCKS):
            rect = pygame.Rect(x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(display_surf, board[y][x], rect)


def rotate_block(block):
    """
    Rotates the block around the center of a 4x4 picture, should expand this so that 3x3 blocks
    rotates correctly
    """
    assert len(block) == 4
    assert len(block[0]) == 4
    new_block = [[BLACK for i in range(4)] for j in range(4)]
    for x in range(4):
        for y in range(4):
            new_block[x][3-y] = block[y][x]
    return new_block


if __name__ == "__main__":
    main()