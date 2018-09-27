
import pygame
import sys
from math import cos, sin, radians
import time
import random
from pygame.locals import *

FPS = 30
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
        'y': 400,
        'width': 4,
        'height': 4,
        'speed': 5,
        'dir': 300
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
    
    while True:  # main game loop
        display_surf.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        move_paddle()
        move_ball()

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


def move_ball():
    
    new_ball_x = ball[X] + cos(radians(ball[DIR])) * ball[SPEED]
       
    
    new_ball_y = ball[Y] - sin(radians(ball[DIR])) * ball[SPEED]
    check_collision(new_ball_x, new_ball_y, True) 
    check_collision(new_ball_x, new_ball_y, False)
    

def check_border(x, y, vertical):

    collision = False

    if vertical:
       if x > WINDOW_WIDTH - ball[WIDTH]:
           ball[X] = WINDOW_WIDTH - ball[WIDTH]
           bounce(vertical)
           collision = True
       elif x < 0:
           ball[X] = 0
           bounce(True)
           collision = True
       else:
           ball[X] = x 
    else:
        if y > WINDOW_HEIGHT - ball[HEIGHT]:
            ball[Y] = WINDOW_HEIGHT - ball[HEIGHT]
            bounce(False)
            collision = True
            # loose ball
        elif y < 0:
            ball[Y] = 0
            bounce(False)
            collision = True
        else:
            ball[Y] = y

    return collision


def check_paddle(x, y, vertical):

    if check_rect_collision(x, y, paddle):
        
        if vertical:
            if paddle[X] + paddle[WIDTH]/2 > x:
                ball[X] = paddle[X] - ball[WIDTH]
            else:
                ball[X] = paddle[X] + paddle[WIDTH]
        else:
            if paddle[Y] + paddle[HEIGHT]/2 > y:
                ball[Y] = paddle[Y] - ball[HEIGHT]
            else:
                ball[Y] = paddle[Y] + paddle[HEIGHT]
        bounce(vertical)
        return True
    return False
        

def check_rect_collision(x, y, rect):

    a = x < rect[X] + rect[WIDTH]
    b = x + ball[WIDTH] > rect[X]
    c = y < rect[Y] + rect[HEIGHT]
    d = y + ball[HEIGHT] > rect[Y]
    
    return a and b and c and d


def check_collision(x, y, vertical):
    
    if check_border(x, y, vertical):
        w = 0
    elif check_paddle(x, y, vertical):
        w = 0


def bounce(virtical):
    if virtical :
        ball[DIR] = (180 - ball[DIR]) % 360
    elif not virtical:
        ball[DIR] = 360 - ball[DIR]


#def correct_ball_placement(x, y, vertical)


def show_game_over_screen(display_surf):
    gameover_surf = pygame.font.Font("freesansbold.ttf", 30).render('Game Over', True, WHITE)
    gameover_rect = gameover_surf.get_rect()
    gameover_rect.topleft = (WINDOW_WIDTH / 2 - gameover_rect.width / 2, WINDOW_HEIGHT / 2 - gameover_rect.height / 2)
    display_surf.blit(gameover_surf, gameover_rect)
    pygame.display.update()
    pygame.event.get()  # Clear the event queue
    while True:  # Wait for a keypress
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return


if __name__ == "__main__":
    main()
