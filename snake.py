import pygame
import random

# CONSTANTS
WIDTH, HEIGHT = 800, 680
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIME = (0, 255, 0)
RED = (255, 0, 0)

BOX_SIDE_LENGTH = 40
FULL_BOX_WIDTH = 0
EMPTY_BOX_WIDTH = 1

STARTING_GRID_X = 0
STARTING_GRID_Y = 0

STARTING_SNAKE_INDEX = 194
STARTING_APPLE_INDEX = 50


# CLASSES
class Box(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_position = None
        self.color = BLACK
        self.width = EMPTY_BOX_WIDTH


class Grid(object):
    grid = []

    def __init__(self):
        self.fill_grid_list()

    def fill_grid_list(self):
        continuing_x = STARTING_GRID_X
        continuing_y = STARTING_GRID_Y

        while continuing_y < HEIGHT:
            while continuing_x < WIDTH:
                box = Box(continuing_x, continuing_y)
                Grid.grid.append(box)
                box.grid_position = Grid.grid.index(box)
                continuing_x += BOX_SIDE_LENGTH
            continuing_x = STARTING_GRID_X
            continuing_y += BOX_SIDE_LENGTH

    def draw_grid(self):
        for box in Grid.grid:
            pygame.draw.rect(WIN, box.color, pygame.Rect(box.x, box.y,
                             BOX_SIDE_LENGTH, BOX_SIDE_LENGTH), box.width)


class Snake(object):
    snake = []

    def __init__(self):
        self.make_snake_head()

    def make_snake_head(self):
        snake_head_grid_box = Grid.grid[STARTING_SNAKE_INDEX]
        snake_head = Box(snake_head_grid_box.x,
                         snake_head_grid_box.y)
        snake_head.grid_position = STARTING_SNAKE_INDEX
        snake_head.direction = "left"
        Snake.snake.append(snake_head)

    def assign_snake_positions(self):
        for snake_box in Snake.snake:
            for box in Grid.grid:
                if (snake_box.x, snake_box.y) == (box.x, box.y):
                    snake_box.grid_position = Grid.grid.index(box)

    def match_snake_with_grid(self):
        for snake_box in Snake.snake:
            for box in Grid.grid:
                if (snake_box.x, snake_box.y) == (box.x, box.y):
                    box.color = LIME
                    box.width = FULL_BOX_WIDTH

    def move_snake(self):
        self.assign_snake_positions()
        snake_head = Snake.snake[0]
        new_coord_x = snake_head.x
        new_coord_y = snake_head.y

        if snake_head.direction == "left":
            new_coord_x -= BOX_SIDE_LENGTH
        elif snake_head.direction == "right":
            new_coord_x += BOX_SIDE_LENGTH
        elif snake_head.direction == "up":
            new_coord_y -= BOX_SIDE_LENGTH
        elif snake_head.direction == "down":
            new_coord_y += BOX_SIDE_LENGTH
        new_coordinates = (new_coord_x, new_coord_y)

        for snake_box in Snake.snake:
            temporary_coordinates = (snake_box.x, snake_box.y)
            old_grid_position = Grid.grid[snake_box.grid_position]
            old_grid_position.color = BLACK
            old_grid_position.width = EMPTY_BOX_WIDTH
            snake_box.x, snake_box.y = new_coordinates
            new_coordinates = temporary_coordinates
        self.assign_snake_positions()
        self.match_snake_with_grid()

    def extend_snake(self, apple):
        last_index = len(Snake.snake) - 1
        snaketail_x = Snake.snake[last_index].x
        snaketail_y = Snake.snake[last_index].y
        snaketail_grid_position = Snake.snake[last_index].grid_position
        self.move_snake()
        apple.change_apple_position()
        new_box = Box(snaketail_x, snaketail_y)
        new_box.grid_position = snaketail_grid_position
        Snake.snake.append(new_box)


class Apple(object):

    def __init__(self):
        self.apple_box = self.make_apple_box()

    def make_apple_box(self):
        apple_grid_box = Grid.grid[STARTING_APPLE_INDEX]
        apple_box = Box(apple_grid_box.x, apple_grid_box.y)
        apple_box.grid_position = STARTING_APPLE_INDEX
        return apple_box

    def find_random_position(self):
        new_grid_position = random.randint(0, len(Grid.grid) - 1)
        new_position = Grid.grid[new_grid_position]
        return new_position


    def change_apple_position(self):
        valid_position = False
        while not valid_position:
            new_position = self.find_random_position()
            if (new_position.width == EMPTY_BOX_WIDTH):
                apple_grid_box = Grid.grid[self.apple_box.grid_position]
                apple_grid_box.width = FULL_BOX_WIDTH
                apple_grid_box.color = LIME
                valid_position = True
                self.apple_box.grid_position = Grid.grid.index(new_position)
                self.apple_box.x, self.apple_box.y = new_position.x, new_position.y


    def match_apple_with_grid(self):
        for box in Grid.grid:
            if (self.apple_box.x, self.apple_box.y) == (box.x, box.y):
                if (box.width == EMPTY_BOX_WIDTH):
                    box.color = RED
                    box.width = FULL_BOX_WIDTH


def draw_window(grid):
    WIN.fill(WHITE)
    grid.draw_grid()
    pygame.display.update()


# MAIN
def main():
    grid = Grid()
    snake = Snake()
    global snake_head
    snake_head = Snake.snake[0]
    apple = Apple()

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(8)
        direction_changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if direction_changed is False:
                    if event.key == pygame.K_LEFT:
                        if snake_head.direction != "right":
                            snake_head.direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        if snake_head.direction != "left":
                            snake_head.direction = "right"
                    elif event.key == pygame.K_UP:
                        if snake_head.direction != "down":
                            snake_head.direction = "up"
                    elif event.key == pygame.K_DOWN:
                        if snake_head.direction != "up":
                            snake_head.direction = "down"
                    direction_changed = True
        draw_window(grid)
        snake.move_snake()
        if (snake_head.grid_position == apple.apple_box.grid_position):
            snake.extend_snake(apple)
        for x in range(1, len(Snake.snake) - 1):
            if (snake_head.grid_position == Snake.snake[x].grid_position):
                run = False
        for snake_box in Snake.snake:
            if snake_box.x < 0 or snake_box.x > 800:
                run = False
            if snake_box.y < 0 or snake_box.y > 680:
                run = False
        apple.match_apple_with_grid()

main()
