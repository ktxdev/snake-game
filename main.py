import sys
import math
import pygame

from enum import Enum
from random import randrange
from collections import deque

# Initialize pygame
pygame.init()

# Window Dimensions
MARGIN = 10
MARGIN_LEFT = 200
WINDOW_WIDTH = 600 + MARGIN
WINDOW_HEIGHT = 420 + (MARGIN * 2)
# Grid Dimensions
GRID_WIDTH = WINDOW_WIDTH - MARGIN_LEFT - MARGIN
GRID_HEIGHT = WINDOW_HEIGHT - (MARGIN * 2)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLOCK_SIZE = 20

# Colors
BLACK = (245, 245, 245)
WHITE = (20, 20, 20)
GREEN = (59, 193, 74)

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

direction = Direction.LEFT

score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)

snake = deque([])
snake_y = (MARGIN * 2) + (GRID_HEIGHT / 2)
snake_x = (MARGIN_LEFT + (GRID_WIDTH / 2))

clock = pygame.time.Clock()

food_x = randrange(MARGIN_LEFT, MARGIN_LEFT + GRID_WIDTH, BLOCK_SIZE)
food_y = randrange(MARGIN, MARGIN + GRID_HEIGHT, BLOCK_SIZE)

game_over_font = pygame.font.Font('freesansbold.ttf', 50)

def place_food(x, y):
    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(SCREEN, (241, 162, 8), rect)

def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    if distance == 0:
        return True
    
    return False

def init_snake(x, y):
    global snake

    for i in range(3):
        x += (BLOCK_SIZE * i)
        snake.append((x, y))

# Draw snake
def draw_snake():
    for (x, y) in snake:
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (231, 90, 124), rect)
    

# Display score
def display_score(x, y):
    score = score_font.render(str.format("Score: {}", score_value), True, BLACK)
    SCREEN.blit(score, (x, y))

# Draw grid
def draw_grid():
    for x in range(MARGIN_LEFT, MARGIN_LEFT + GRID_WIDTH - MARGIN, BLOCK_SIZE):
        for y in range(MARGIN, WINDOW_HEIGHT - MARGIN, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, GREEN, rect, 1)

def game_over():
    x = ((GRID_WIDTH + (MARGIN * 2)) / 2) - 32
    y = ((MARGIN + (GRID_HEIGHT / 2))) - 32

    game_over_text = score_font.render("GAME OVER !!!", True, BLACK)
    SCREEN.blit(game_over_text, (x, y))

init_snake(snake_x, snake_y)

running = True
is_game_over = False
while running:
    clock.tick(5)

    SCREEN.fill((78, 110, 93))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not is_game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != Direction.RIGHT:
            direction = Direction.LEFT
        elif keys[pygame.K_RIGHT] and direction != Direction.LEFT:
            direction = Direction.RIGHT
        elif keys[pygame.K_UP] and direction != Direction.DOWN:
            direction = Direction.UP
        elif keys[pygame.K_DOWN] and direction != Direction.UP:
            direction = Direction.DOWN

        # Draw grid
        draw_grid()

        # Display score
        display_score(10, 10)

        if direction == Direction.LEFT:
            snake_x = snake[0][0] - BLOCK_SIZE

            if snake_x < MARGIN_LEFT:
                snake_x = MARGIN_LEFT + GRID_WIDTH - BLOCK_SIZE

            snake.appendleft((snake_x, snake[0][1]))

        elif direction == Direction.UP:
            snake_y = snake[0][1] - BLOCK_SIZE
            
            if snake_y < MARGIN:
                snake_y = MARGIN + GRID_HEIGHT - BLOCK_SIZE

            snake.appendleft((snake[0][0], snake_y))

        elif direction == Direction.RIGHT:
            snake_x = snake[0][0] + BLOCK_SIZE

            if snake_x > (WINDOW_WIDTH - MARGIN - BLOCK_SIZE):
                snake_x = MARGIN_LEFT

            snake.appendleft((snake_x, snake[0][1]))

        elif direction == Direction.DOWN:
            snake_y = snake[0][1] + BLOCK_SIZE

            if snake_y > (WINDOW_HEIGHT - MARGIN - BLOCK_SIZE):
                snake_y = MARGIN

            snake.appendleft((snake[0][0], snake_y))

        ate_food = is_collision(food_x, food_y, snake[0][0], snake[0][1])
        if not ate_food:
            snake.pop()
        else:
            score_value += 1
            snake_points = set(snake)

            food_x = randrange(MARGIN_LEFT, MARGIN_LEFT + GRID_WIDTH, BLOCK_SIZE)
            food_y = randrange(MARGIN, MARGIN + GRID_HEIGHT, BLOCK_SIZE)

            while((food_x, food_y) in snake_points):
                food_x = randrange(MARGIN_LEFT, MARGIN_LEFT + GRID_WIDTH, BLOCK_SIZE)
                food_y = randrange(MARGIN, MARGIN + GRID_HEIGHT, BLOCK_SIZE)

            del snake_points

        # Draw snake
        draw_snake()

        # Place food
        place_food(food_x, food_y)

        if len(snake) >= 4:
            for i in range(4, len(snake)):
                x, y = snake[i]

                snake_ate_self = is_collision(x, y, snake[0][0], snake[0][1])

                if snake_ate_self:
                    game_over()
                    is_game_over = True
                    break

        # Update screen
        pygame.display.update()
    