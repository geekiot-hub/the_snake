from abc import ABC, abstractclassmethod
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject(ABC):
    GRID_HEIGHT: int = GRID_HEIGHT
    GRID_WIDTH: int = GRID_WIDTH
    GRID_SIZE: int = GRID_SIZE
    COLOR: tuple
    BORDER_COLOR: tuple

    def __init__(
        self, color: tuple, border_color: tuple, position: list = None
    ):
        self.COLOR = color
        self.BORDER_COLOR = border_color
        self.position_ = position or [self.generate_random_position()]

    def generate_random_position(self) -> list[int]:
        return [
            randint(0, self.GRID_WIDTH - 1),
            randint(0, self.GRID_HEIGHT - 1),
        ]

    @abstractclassmethod
    def draw(cls):
        pass


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move(self):
        pass

    def draw(self):
        pass

    def update_keys(self):
        pass


class Apple(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_position(self):
        self.position_ = self.generate_random_position()

    @property
    def position(self):
        return self.position_[0]

    @position.setter
    def position(self, value: int):
        self.position_[0] = value

    def draw(self):
        rect = pygame.Rect(
            self.position, (self.GRID_SIZE, self.GRID_SIZE)
        )
        pygame.draw.rect(screen, self.COLOR, rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, rect, 1)


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(color=SNAKE_COLOR, border_color=BORDER_COLOR)
    apple = Apple(color=APPLE_COLOR, border_color=BORDER_COLOR)

    while True:
        snake.update_keys()
        snake.move()

        snake.draw()
        apple.draw()

        clock.tick(SPEED)

    # Тут опишите основную логику игры.
    # ...


if __name__ == "__main__":
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
