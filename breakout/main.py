
import pygame
import sys
import math
import time
import random
from pygame.locals import *

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

PADDLE_STARTING_WIDTH = 50
PADDLE_HEIGHT = 10
PADDLE_STARTING_SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = BLACK

X = 'x'
Y = 'y'
WIDTH = 'width'
HEIGHT = 'height'
SPEED = 'speed'
DIR = 'dir'

paddle = {'x': WINDOW_WIDTH/2 - PADDLE_STARTING_WIDTH/2,
          'y': WINDOW_HEIGHT - PADDLE_HEIGHT/2 - 10,
          'width': PADDLE_STARTING_WIDTH,
          'height': PADDLE_HEIGHT,
          'speed': PADDLE_STARTING_SPEED}

ball = {'x': WINDOW_WIDTH/2,
        'y': WINDOW_HEIGHT/2,
        'width': 4,
        'height': 4,
        'speed': 4,
        'dir': 90
        }


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("breakout")

    while True:
        run_game(display_surf, fps_clock)
        show_game_over_screen(display_surf)


def run_game(display_surf, fps_clock):
    """ Runs an entire instance of the game, returns when someone wins. """
    global paddle
    global ball

    while True:  # main game loop
        display_surf.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        paddle = move_paddle()
        ball = move_ball()

        # create rectangles for easier collision detection
        paddle_rect = pygame.Rect(paddle[X], paddle[Y], paddle[WIDTH], paddle[HEIGHT])
        ball_rect = pygame.Rect(ball[X], ball[Y], ball[WIDTH], ball[HEIGHT])

        draw_game(display_surf, paddle_rect, ball_rect)

        fps_clock.tick(FPS)


def draw_game(display_surf, paddle_rect, ball_rect):
    """ Draws the entirety of the game. """

    draw_paddle(display_surf, paddle_rect)
    draw_ball(display_surf, ball_rect)
    pygame.display.update()


def draw_paddle(display_surf, paddle_rect):
    pygame.draw.rect(display_surf, WHITE, paddle_rect)

def draw_ball(display_surf, ball_rect):
    pygame.draw.rect(display_surf,WHITE,ball_rect)

def move_paddle():
    global paddle
    """
    Moves the paddles according to the buttons pressed.
    A and D moves the left paddle, and UP and DOWN moves
    the right.
    """
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        new_paddle_y = paddle[X] - paddle[SPEED]
        paddle[X] = new_paddle_y if new_paddle_y > 0 else 0
    elif keys[K_d]:
        new_paddle_y = paddle[X] + paddle[SPEED]
        paddle[X] = new_paddle_y if new_paddle_y < WINDOW_WIDTH - paddle[WIDTH] else WINDOW_WIDTH - paddle[WIDTH]
    return paddle


def move_ball():
    global ball

    new_ball_x = ball[X] + math.cos(math.radians(ball[DIR])) * ball[SPEED]
    new_ball_y = ball[Y] - math.sin(math.radians(ball[DIR])) * ball[SPEED]
    x_multi = -1 if math.cos(math.radians(ball[DIR])) < 0 else 1

    ball = check_collition(new_ball_x, new_ball_y)

    return ball


def check_collition(x, y):
    global ball

    if x > WINDOW_WIDTH - ball[WIDTH]:
        ball[X] = WINDOW_WIDTH - ball[WIDTH]
    elif x < 0:
        ball[X] = 0
    else:
        ball[X] = x

    if y > WINDOW_HEIGHT - ball[HEIGHT]:
        ball[Y] = WINDOW_HEIGHT - ball[HEIGHT]  # loose ball
    elif y < 0:
        ball[Y] = 0
    else:
        ball[Y] = y

    return ball


def handle_collisin(ball, )


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


if __name__ == "__main__":
    main()
