"""
A Pong game written in Python using pygame.
Written by Mattias Salo salo.mattias@gmail.com
"""

import pygame
import sys
import math
import time
import random
from pygame.locals import *

FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BALL_SIDE = 10
BALL_SPEED = 5
PADDLE_LENGTH = 50
PADDLE_WIDTH = 10
PADDLE_SPEED = 5
LEFT_PADDLE_X = 10
RIGHT_PADDLE_X = WINDOW_WIDTH - LEFT_PADDLE_X - PADDLE_WIDTH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = BLACK

LEFT = "left"
RIGHT = "right"


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong")

    left_score = 0
    right_score = 0
    collision_counter = 0
    ball_speed = BALL_SPEED

    x_speed, y_speed = random_ball_start()

    l_paddle_y = WINDOW_HEIGHT / 2 - PADDLE_LENGTH / 2
    r_paddle_y = WINDOW_HEIGHT / 2 - PADDLE_LENGTH / 2

    x = int(WINDOW_WIDTH / 2)
    y = int(WINDOW_HEIGHT / 2)

    while True:  # main game loop
        display_surf.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        l_paddle_y, r_paddle_y = move_paddles(l_paddle_y, r_paddle_y)

        x = x + x_speed

        new_y = y + y_speed
        if new_y > WINDOW_HEIGHT - BALL_SIDE or new_y < 0:
            y_speed *= -1
        y = y + y_speed

        ball_rect = pygame.Rect(x, y, BALL_SIDE, BALL_SIDE)
        l_paddle_rect = pygame.Rect(LEFT_PADDLE_X, l_paddle_y, PADDLE_WIDTH, PADDLE_LENGTH)
        r_paddle_rect = pygame.Rect(RIGHT_PADDLE_X, r_paddle_y, PADDLE_WIDTH, PADDLE_LENGTH)

        collision = collision_detect(ball_rect, l_paddle_rect, r_paddle_rect, x_speed, y_speed, BALL_SPEED)

        if collision == RIGHT:
            x_speed, y_speed = handle_r_paddle_collision(ball_rect, r_paddle_rect, ball_speed)
            collision_counter += 1
        elif collision == LEFT:
            x_speed, y_speed = handle_l_paddle_collision(ball_rect, l_paddle_rect, ball_speed)
            collision_counter += 1

        ball_speed = BALL_SPEED + int(collision_counter / 4)

        if check_score(ball_rect):
            x_speed, y_speed = random_ball_start()
            x, y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
            ball_speed = BALL_SPEED
            collision_counter = 0
            if check_score(ball_rect) == LEFT:
                left_score += 1
            else:
                right_score += 1
            time.sleep(2)

        draw_game(display_surf, left_score, right_score, ball_rect, l_paddle_rect, r_paddle_rect)

        if left_score == 7 or right_score == 7:
            show_game_over_screen(display_surf, pygame.font.Font("freesansbold.ttf", 18))
            left_score = 0
            right_score = 0
            l_paddle_y = WINDOW_HEIGHT / 2 - PADDLE_LENGTH / 2
            r_paddle_y = WINDOW_HEIGHT / 2 - PADDLE_LENGTH / 2

        fps_clock.tick(FPS)


def draw_game(display_surf, left_score, right_score, ball_rect, l_paddle_rect, r_paddle_rect):
    font = pygame.font.Font("freesansbold.ttf", 18)
    left_score_surf = font.render("%s" % left_score, True, WHITE)
    left_score_rect = left_score_surf.get_rect()
    left_score_rect.topleft = (0, 0)

    right_score_surf = font.render("%s" % right_score, True, WHITE)
    right_score_rect = right_score_surf.get_rect()
    right_score_rect.topright = (WINDOW_WIDTH, 0)

    display_surf.blit(left_score_surf, left_score_rect)
    display_surf.blit(right_score_surf, right_score_rect)
    draw_ball(display_surf, ball_rect)
    draw_paddle(display_surf, l_paddle_rect)
    draw_paddle(display_surf, r_paddle_rect)
    pygame.display.update()


def draw_ball(display_surf, ball_rect):
    pygame.draw.rect(display_surf, WHITE, ball_rect)


def draw_paddle(display_surf, paddle_rect):
    pygame.draw.rect(display_surf, WHITE, paddle_rect)


def move_paddles(l_paddle_y, r_paddle_y):
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        new_paddle_y = l_paddle_y - PADDLE_SPEED
        l_paddle_y = new_paddle_y if new_paddle_y > -PADDLE_LENGTH else -PADDLE_LENGTH
    elif keys[K_s]:
        new_paddle_y = l_paddle_y + PADDLE_SPEED
        l_paddle_y = new_paddle_y if new_paddle_y < WINDOW_HEIGHT else WINDOW_HEIGHT
    if keys[K_UP]:
        new_paddle_y = r_paddle_y - PADDLE_SPEED
        r_paddle_y = new_paddle_y if new_paddle_y > -PADDLE_LENGTH else -PADDLE_LENGTH
    elif keys[K_DOWN]:
        new_paddle_y = r_paddle_y + PADDLE_SPEED
        r_paddle_y = new_paddle_y if new_paddle_y < WINDOW_HEIGHT else WINDOW_HEIGHT
    return l_paddle_y, r_paddle_y


def random_ball_start():
    angle = random.randint(0, 360)
    while (45 < angle < 135) or (225 < angle < 315):
        angle = random.randint(0, 360)
    x_speed = int(math.cos(math.radians(angle)) * BALL_SPEED)
    y_speed = int(math.sin(math.radians(angle)) * BALL_SPEED)
    return x_speed, y_speed


def collision_detect(ball, left_paddle, right_paddle, speed_x, speed_y, speed):
    if ball.colliderect(right_paddle):
        return RIGHT
    if ball.colliderect(left_paddle):
        return LEFT
    return False


def handle_l_paddle_collision(ball, paddle, speed):

    relative_position = (paddle.y + (PADDLE_LENGTH / 2)) - (ball.y + (BALL_SIDE / 2))
    normalised_relative_position = relative_position / (PADDLE_LENGTH / 2)
    bounce = normalised_relative_position * 50
    return int(math.cos(math.radians(bounce)) * speed), int(-math.sin(math.radians(bounce)) * speed)


def handle_r_paddle_collision(ball, paddle, speed):

    relative_position = (paddle.y + (PADDLE_LENGTH / 2)) - (ball.y + (BALL_SIDE / 2))
    normalised_relative_position = relative_position / (PADDLE_LENGTH / 2)
    bounce = normalised_relative_position * 50
    return int(-math.cos(math.radians(bounce)) * speed), int(-math.sin(math.radians(bounce)) * speed)


def check_score(ball):
    if ball.x < 0:
        return RIGHT
    elif ball.x + BALL_SIDE > WINDOW_WIDTH:
        return LEFT
    else:
        return False


def show_game_over_screen(display_surf, basic_font):
    """ Shows the game over screen over the game board. """
    game_over_font = pygame.font.Font("freesansbold.ttf", 150)
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
