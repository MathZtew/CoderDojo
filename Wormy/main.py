"""
Based on:
          Wormy (a Nibbles clone)
          By Al Sweigart al@inventwithpython.com
          http://inverntwithpython.com/pygame
          Creative Commons BY-NC-SA 3.0 US

This game is licensed under Creative Commons BY-NC-SA 3.0 US
modifications and rewritten by:
Mattias Salo salo.mattias@gmail.com
"""

import random
import pygame
import sys

from pygame.locals import *

BASE_FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
MIN_FPS = 5
SCORE_DIVIDER = 3

FONT = 'freesansbold.ttf'

assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size"
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size"

CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

#        R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
DARK_GRAY = (40, 40, 40)
BG_COLOR = BLACK

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0  # syntactic sugar: index of the worms head


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    basic_font = pygame.font.Font(FONT, 18)
    pygame.display.set_caption('Wormy')

    show_start_screen(display_surf, basic_font, fps_clock)
    while True:
        run_game(display_surf, basic_font, fps_clock)
        show_game_over_screen(display_surf, basic_font)


def run_game(display_surf, basic_font, fps_clock):
    """
    Starts an instance of the game and runs the whole game loop uninterrupted.
    """
    # Set starting values
    worm_coords = random_start_point()
    apple = get_random_apple_location(worm_coords)
    direction = RIGHT

    while True:  # main game loop
        direction = handle_events(direction)

        if is_worm_hit(worm_coords):
            return  # game over

        if has_worm_eaten_apple(worm_coords, apple):
            # don't remove worm's tail segment
            apple = get_random_apple_location(worm_coords)
        else:
            # remove worms tail segment
            del worm_coords[-1]

        new_head = move_worm(direction, worm_coords)
        worm_coords.insert(0, new_head)

        score = len(worm_coords) - 3
        
        draw_game(display_surf, basic_font, worm_coords, apple, score)
        
        # base the speed of the game on the score
        new_fps = MIN_FPS + int(score / SCORE_DIVIDER)
        fps = new_fps if new_fps < BASE_FPS else BASE_FPS
        fps_clock.tick(fps)


def handle_events(direction):
    """
    handles keypresses and program exits

    :param direction: The direction of the worm
    :return: A new direction if a relevant key has been pressed otherwise the same direction
    """
    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                return LEFT
            elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                return RIGHT
            elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                return UP
            elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                return DOWN
            elif event.key == K_ESCAPE:
                terminate()
    return direction


def is_worm_hit(worm_coords):
    """
    Checks whether the worm is hit and if the game is to be ended.
    :param worm_coords: the coordinates of the worm
    :return: Boolean, if the worm is hit
    """
    if worm_coords[HEAD]['x'] == -1 or worm_coords[HEAD]['x'] == CELL_WIDTH \
            or worm_coords[HEAD]['y'] == -1 or worm_coords[HEAD]['y'] == CELL_HEIGHT:
        return True
    for worm_body in worm_coords[1:]:
        if worm_body['x'] == worm_coords[HEAD]['x'] and worm_body['y'] == worm_coords[HEAD]['y']:
            return True
    
    
def has_worm_eaten_apple(worm_coords, apple):
    """ Checks whether the worm is in a position to eat the apple. """
    return worm_coords[HEAD]['x'] == apple['x'] and worm_coords[HEAD]['y'] == apple['y']


def move_worm(direction, worm_coords):
    """
    Moves the worm in the direction specified.

    :return: New position for the head.
    """
    if direction == UP:
        return {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        return {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        return {'x': worm_coords[HEAD]['x'] - 1, 'y': worm_coords[HEAD]['y']}
    elif direction == RIGHT:
        return {'x': worm_coords[HEAD]['x'] + 1, 'y': worm_coords[HEAD]['y']}


def random_start_point():
    """
    Creates a new worm of size 3 in a random location.
    """
    start_x = random.randint(5, CELL_WIDTH - 6)
    start_y = random.randint(5, CELL_HEIGHT - 6)
    return [
        {'x': start_x, 'y': start_y},
        {'x': start_x - 1, 'y': start_y - 1},
        {'x': start_x - 2, 'y': start_y - 2}
    ]


def draw_game(display_surf, basic_font, worm_coords, apple, score):
    """ Draws the game to the screen """
    display_surf.fill(BG_COLOR)
    draw_grid(display_surf)
    draw_worm(worm_coords, display_surf)
    draw_apple(apple, display_surf)
    draw_score(score, display_surf, basic_font)
    pygame.display.update()


def draw_press_key_msg(display_surf, basic_font):
    """ Shows a message to the player to press a key. """
    press_key_surf = basic_font.render('Press a key to play', True, DARK_GRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    display_surf.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    """ Checks whether a key has been pressed and exits if quit has been pressed. """
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_start_screen(display_surf, basic_font, fps_clock):
    """ Shows the animated start screen. """
    title_font = pygame.font.Font(FONT, 100)
    title_surf1 = title_font.render('Wormy!', True, WHITE, DARK_GREEN)
    title_surf2 = title_font.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        display_surf.fill(BG_COLOR)
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        display_surf.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        display_surf.blit(rotated_surf2, rotated_rect2)

        draw_press_key_msg(display_surf, basic_font)

        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        fps_clock.tick(BASE_FPS)
        degrees1 += 1  # rotate by 3 degrees each frame
        degrees2 += 2  # rotate by 7 degrees each frame


def terminate():
    """ Exits the program. """
    pygame.quit()
    sys.exit()


def get_random_location():
    """ Sets a random location within the board. """
    return {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}


def get_random_apple_location(worm_coords):
    """ Sets a random location on the board that does not collide with the worm. """
    collision = True
    location = get_random_location()
    while collision:
        collision = False
        location = get_random_location()
        for worm_body in worm_coords:
            if worm_body['x'] == location['x'] and worm_body['y'] == location['y']:
                collision = True
    return location


def show_game_over_screen(display_surf, basic_font):
    """ Shows the game over screen over the game board. """
    game_over_font = pygame.font.Font(FONT, 150)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    display_surf.blit(game_surf, game_rect)
    display_surf.blit(over_surf, over_rect)
    draw_press_key_msg(display_surf, basic_font)
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()  # clear out any key presses in the event queue

    while True:
        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return


def draw_score(score, display_surf, basic_font):
    """ draws the score in the top left corner. """
    score_surf = basic_font.render('Score: %s' % score, True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    display_surf.blit(score_surf, score_rect)


def draw_worm(worm_coords, display_surf):
    """ Draws the worm in the corresponding place. """
    for coord in worm_coords:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(display_surf, DARK_GREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(display_surf, GREEN, worm_inner_segment_rect)


def draw_apple(coord, display_surf):
    """ Draws the apple on the game board. """
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(display_surf, RED, apple_rect)


def draw_grid(display_surf):
    """ Draws the supporting grid on the game board. """
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(display_surf, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(display_surf, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))


if __name__ == "__main__":
    main()
