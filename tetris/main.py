import pygame
import sys
from pygame.locals import *
import random

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60

VERTICAL_BLOCKS = 20
HORIZONTAL_BLOCKS = 10

assert WINDOW_HEIGHT % VERTICAL_BLOCKS == 0
assert WINDOW_WIDTH % HORIZONTAL_BLOCKS == 0

CELL_SIZE = int(WINDOW_HEIGHT / VERTICAL_BLOCKS)

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
J = [[BLUE, BLACK, BLACK],
     [BLUE, BLUE, BLUE],
     [BLACK, BLACK, BLACK]]
L = [[BLACK, BLACK, ORANGE],
     [ORANGE, ORANGE, ORANGE],
     [BLACK, BLACK, BLACK]]
O = [[BLACK, BLACK, BLACK, BLACK],
     [BLACK, YELLOW, YELLOW, BLACK],
     [BLACK, YELLOW, YELLOW, BLACK],
     [BLACK, BLACK, BLACK, BLACK]]
S = [[BLACK, BLACK, BLACK],
     [BLACK, GREEN, GREEN],
     [GREEN, GREEN, BLACK]]
T = [[BLACK, BLACK, BLACK],
     [BLACK, PURPLE, BLACK],
     [PURPLE, PURPLE, PURPLE]]
Z = [[BLACK, BLACK, BLACK],
     [RED, RED, BLACK],
     [BLACK, RED, RED]]

BLOCKS = [I, J, L, O, S, T, Z]

NAME = "Tetris"


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(NAME)

    while True:
        run_game(display_surf, fps_clock)
        show_game_over_screen(display_surf)


def run_game(display_surf, fps_clock):
    board = [[BLACK for i in range(HORIZONTAL_BLOCKS)] for j in range(VERTICAL_BLOCKS)]
    show_next_board = [[BLACK for i in range(4)] for j in range(4)]

    points = 0
    lines_cleared = 0
    level = 0
    wait_frames = get_wait_frames(level)
    frame = 0
    accelerate = False

    falling_block = get_random_block()
    falling_block = set_block_coordinates(falling_block)
    next_block = get_random_block()

    while True:  # main game loop

        if frame == wait_frames:
            falling_block['y'] += 1
            if is_collision(board, falling_block):
                # Return block to previous position
                falling_block['y'] -= 1
                add_block_to_board(board, falling_block)
                # Get a new block
                falling_block = next_block
                falling_block = set_block_coordinates(falling_block)
                next_block = get_random_block()

                lines_to_remove = get_lines_to_remove(board)
                board = clear_lines(board, lines_to_remove)

                if len(lines_to_remove):
                    points += get_points(len(lines_to_remove), level)
                    lines_cleared += len(lines_to_remove)
                    level = get_level(lines_cleared)

                    # update the wait frames if there's been a level shift
                    wait_frames = get_wait_frames(level)

                if is_collision(board, falling_block):
                    return  # Game over if there's a collision in the newly spawned block
            frame = 0
        else:
            frame += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    falling_block['block'] = rotate_block(falling_block['block'])
                    if is_collision(board, falling_block):
                        for i in range(3):
                            falling_block['block'] = rotate_block(falling_block['block'])
                if event.key == K_LEFT:
                    falling_block['x'] -= 1
                    if is_collision(board, falling_block):
                        falling_block['x'] += 1
                if event.key == K_RIGHT:
                    falling_block['x'] += 1
                    if is_collision(board, falling_block):
                        falling_block['x'] -= 1
                if event.key == K_SPACE:
                    while not is_collision(board, falling_block):
                        falling_block['y'] += 1
                    falling_block['y'] -= 1
                    frame = wait_frames
                if event.key == K_DOWN:
                    wait_frames = 3 if get_wait_frames(level) > 3 else get_wait_frames(level)
                    frame = frame if frame <= 3 else 0
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    wait_frames = get_wait_frames(level)

        display_surf.fill(BLACK)
        draw_game(display_surf, board, falling_block, points, level, next_block, show_next_board)
        # Last thing to be done
        pygame.display.update()
        fps_clock.tick(FPS)


def draw_game(display_surf, board, falling_block, score, level, next_block, show_next_board):
    """ Draws the game """
    draw_board(display_surf, board, falling_block, 0, 0)
    draw_grid(display_surf)
    draw_score(display_surf, score, level, next_block, show_next_board)


def draw_grid(display_surf):
    """ Draws the supporting grid on the game board. """
    for x in range(0, CELL_SIZE * (HORIZONTAL_BLOCKS + 1), CELL_SIZE):  # draw vertical lines
        pygame.draw.line(display_surf, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, CELL_SIZE * (VERTICAL_BLOCKS + 1), CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(display_surf, WHITE, (0, y), (CELL_SIZE * HORIZONTAL_BLOCKS, y))
    # Draw the last horizontal line
    pygame.draw.line(display_surf, WHITE, (0, WINDOW_HEIGHT - 1), (CELL_SIZE * HORIZONTAL_BLOCKS, WINDOW_HEIGHT - 1))


def draw_board(display_surf, board, block, start_x, start_y):
    """ Draws the whole game board, where the board is an array of colours """
    for x in range(len(board[0])):
        for y in range(len(board)):
            rect = pygame.Rect(start_x + x * CELL_SIZE, start_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            block_color = get_block_color(x, y, block)
            if block_color != BLACK:
                pygame.draw.rect(display_surf, block_color, rect)
            else:
                pygame.draw.rect(display_surf, board[y][x], rect)


def get_block_color(x, y, block):
    """ Gets the block colour of the coordinates, if nothing is there returns BLACK """
    x_diff = x - block['x']
    y_diff = y - block['y']
    side = block['side']
    if 0 <= x_diff < side and 0 <= y_diff < side:
        return block['block'][y_diff][x_diff]
    return BLACK


def is_collision(board, falling_block):
    """
    Checks whether there is a collision with the board and the block,
    there is a collision if the block is out of bounds.
    """
    for x in range(falling_block['x'], falling_block['x'] + falling_block['side']):
        for y in range(falling_block['y'], falling_block['y'] + falling_block['side']):
            block_color = get_block_color(x, y, falling_block)
            if 0 <= x < HORIZONTAL_BLOCKS and y < VERTICAL_BLOCKS:
                if y < 0:  # We don't want to check collisions above the "ceiling"
                    pass
                elif board[y][x] != BLACK and block_color != BLACK:
                    return True
            else:
                if block_color != BLACK:
                    return True
    return False


def rotate_block(block):
    """
    Rotates the block around the center of a square picture.
    """
    height = len(block)
    assert len(block[0]) == height
    new_block = [[BLACK for i in range(height)] for j in range(height)]
    for x in range(height):
        for y in range(height):
            new_block[x][height - 1 - y] = block[y][x]
    return new_block


def add_block_to_board(board, falling_block):
    """
    Adds the falling block to the board at the place where the block is.
    """
    for x in range(falling_block['x'], falling_block['x'] + falling_block['side']):
        for y in range(falling_block['y'], falling_block['y'] + falling_block['side']):
            if x < HORIZONTAL_BLOCKS and y < VERTICAL_BLOCKS:
                block_color = get_block_color(x, y, falling_block)
                board[y][x] = block_color if block_color != BLACK else board[y][x]


def get_random_block():
    """ Get a random block. """
    i = random.randint(0, len(BLOCKS) - 1)
    return {'y': 0, 'x': 0, 'block': BLOCKS[i][:], 'side': len(BLOCKS[i])}


def set_block_coordinates(block):
    block['y'] = -2
    block['x'] = HORIZONTAL_BLOCKS // 2 - 2
    return block


def get_lines_to_remove(board):
    """ Gets the index of the full lines to be removed. """
    lines_to_remove = []
    for i in range(VERTICAL_BLOCKS):
        lines_to_remove.append(i)
        for block in board[i]:
            if block == BLACK:
                lines_to_remove.remove(i)
                break
    return lines_to_remove


def clear_lines(board, lines_to_remove):
    """
    Clears the board of the full lines
    :param board:
    :return: A new board with the full lines gone
    """
    board_copy = board[:]

    for line in lines_to_remove:
        board_copy.pop(line)
        board_copy = [[BLACK for i in range(HORIZONTAL_BLOCKS)]] + board_copy
    return board_copy


def get_points(lines, level):
    """ Gets the points with the help of the numbers of lines cleared and the level of the game. """
    if lines == 1:
        return 100 * (level + 1)
    if lines == 2:
        return 200 * (level + 1)
    if lines == 3:
        return 500 * (level + 1)
    if lines == 4:
        return 800 * (level + 1)
    return 0


def draw_score(display_surf, score, level, next_block, show_next_board):
    """ Draws the score in the upper right corner. """
    font = pygame.font.Font("freesansbold.ttf", 25)
    score_surf = font.render("%s" % score, True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topright = (WINDOW_WIDTH, 0)
    score_lower = score_rect.bottomright[1]
    level_surf = font.render("%s" % level, True, WHITE)
    level_rect = level_surf.get_rect()
    level_rect.topright = (WINDOW_WIDTH, score_lower)
    level_lower = level_rect.bottomright[1]
    display_surf.blit(score_surf, score_rect)
    display_surf.blit(level_surf, level_rect)

    draw_board(display_surf, show_next_board, next_block, WINDOW_WIDTH - CELL_SIZE * 4, level_lower)
    for x in range(WINDOW_WIDTH - CELL_SIZE * 4, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(display_surf, WHITE, (x, level_lower), (x, level_lower + CELL_SIZE * 4))
    for y in range(level_lower, level_lower + CELL_SIZE * 5, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(display_surf, WHITE, (WINDOW_WIDTH - CELL_SIZE * 4, y), (WINDOW_WIDTH, y))


def get_wait_frames(level):
    """
    Get the amount of frames to wait before dropping the block one step.
    Using the frame timings of the NES version.
    """
    if 0 <= level <= 8:
        return 48 - (5 * level)
    if level == 9:
        return 6
    if 10 <= level <= 12:
        return 5
    if 13 <= level <= 15:
        return 4
    if 16 <= level <= 18:
        return 3
    if 19 <= level <= 28:
        return 2
    return 1


def get_level(lines):
    """ Gets the level of the game based on the number of lines cleared. """
    return lines // 10


def show_game_over_screen(display_surf):
    """ Shows the game over screen over the game board. """
    font = pygame.font.Font("freesansbold.ttf", 18)
    game_over_font = pygame.font.Font("freesansbold.ttf", 150)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    display_surf.blit(game_surf, game_rect)
    display_surf.blit(over_surf, over_rect)
    draw_press_key_msg(display_surf, font)
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()  # clear out any key presses in the event queue

    while True:
        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return


def draw_press_key_msg(display_surf, basic_font):
    """ Shows a message to the player to press a key. """
    press_key_surf = basic_font.render('Press a key to play', True, WHITE)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    display_surf.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    """ Checks whether a key has been pressed and exits if quit has been pressed. """
    if len(pygame.event.get(QUIT)) > 0:
        pygame.quit()
        sys.exit()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    return key_up_events[0].key


if __name__ == "__main__":
    main()