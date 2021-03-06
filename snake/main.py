import pygame
import sys
import random
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60  # Frames per second
MIN_FPS = 5
SCORE_DIVIDER = 3
BOX_SIZE = 20
START_WAIT_FRAMES = 20
HOR_BOXES = WINDOW_HEIGHT // BOX_SIZE
VER_BOXES = WINDOW_WIDTH // BOX_SIZE

assert WINDOW_WIDTH % BOX_SIZE == 0
assert WINDOW_HEIGHT % BOX_SIZE == 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# The name of the application
NAME = "CoderSnake"

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


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
        show_game_over(display_surf)


def run_game(display_surf, fps_clock):
    """
    Game loop, one game until game over
    """
    snake = [{"x": 2, "y": 0}, {"x": 1, "y": 0}, {"x": 0, "y": 0}]
    apple = random_apple(snake)
    direction = RIGHT
    new_direction = RIGHT
    wait_frames = START_WAIT_FRAMES
    frame = 0
    score = 0
    
    # main game loop
    while True:
        display_surf.fill(BLACK)
        draw_game(display_surf, snake, apple, score)

        # Handle exit event, so that game can exit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    new_direction = UP
                if event.key == K_DOWN:
                    new_direction = DOWN
                if event.key == K_LEFT:
                    new_direction = LEFT
                if event.key == K_RIGHT:
                    new_direction = RIGHT

        if frame == wait_frames:
            frame = 0
            if can_eat_apple(snake, apple):
                apple = random_apple(snake)
                score += 1
                wait_frames = START_WAIT_FRAMES - score // 2 if START_WAIT_FRAMES - score // 2 > 3 else 3
                snake.append(snake[-1])
            direction = next_direction(direction, new_direction)
            move_snake(snake, direction)
            if is_worm_hit(snake):
                return  # Game over
        else:
            frame += 1

        # This should be on the end of the loop
        pygame.display.update()
        fps_clock.tick(FPS)


def move_snake(snake, direction):
    if direction == UP:
        snake.insert(0, {"x": snake[0]["x"], "y": snake[0]["y"] - 1})
    elif direction == DOWN:
        snake.insert(0, {"x": snake[0]["x"], "y": snake[0]["y"] + 1})
    elif direction == LEFT:
        snake.insert(0, {"x": snake[0]["x"] - 1, "y": snake[0]["y"]})
    elif direction == RIGHT:
        snake.insert(0, {"x": snake[0]["x"] + 1, "y": snake[0]["y"]})
    snake.pop()
    return snake


def next_direction(direction, new_direction):
    if direction == RIGHT:
        return new_direction if new_direction != LEFT else RIGHT
    if direction == LEFT:
        return new_direction if new_direction != RIGHT else LEFT
    if direction == UP:
        return new_direction if new_direction != DOWN else UP
    if direction == DOWN:
        return new_direction if new_direction != UP else DOWN


def random_apple(snake):
    apple = {"x": random.randint(0, VER_BOXES - 1), "y": random.randint(0, HOR_BOXES - 1)}
    while is_apple_in_snake(apple, snake):
        apple = {"x": random.randint(0, VER_BOXES - 1), "y": random.randint(0, HOR_BOXES - 1)}
    return apple


def is_apple_in_snake(apple, snake):
    for body in snake:
        if apple["x"] == body["x"] and apple["y"] == body["y"]:
            return True
    return False


def can_eat_apple(snake, apple):
    return snake[0]["x"] == apple["x"] and snake[0]["y"] == apple["y"]


def is_worm_hit(snake):
    if snake[0]["x"] < 0 or snake[0]["x"] >= VER_BOXES:
        return True
    if snake[0]["y"] < 0 or snake[0]["y"] >= HOR_BOXES:
        return True
    for body in snake[1:]:
        if snake[0]["x"] == body["x"] and snake[0]["y"] == body["y"]:
            return True
    return False


def draw_game(display_surf, snake, apple, score):
    # Draw background
    display_surf.fill(BLACK)
    # Draw apple
    apple_rect = pygame.Rect(apple["x"] * BOX_SIZE, apple["y"] * BOX_SIZE, BOX_SIZE, BOX_SIZE)
    pygame.draw.rect(display_surf, RED, apple_rect)
    # Draw snake
    for body in snake:
        snake_rect = pygame.Rect(body["x"] * BOX_SIZE, body["y"] * BOX_SIZE, BOX_SIZE, BOX_SIZE)
        pygame.draw.rect(display_surf, GREEN, snake_rect)
    # Draw score
    score_surf = pygame.font.Font("freesansbold.ttf", 18).render('Score: %s' % score, True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (0, 0)
    display_surf.blit(score_surf, score_rect)


def show_game_over(display_surf):
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
