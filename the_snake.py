from random import randint

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

# Цвет лука
ONION_COLOR = (255, 255, 255)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для объекта игры."""

    def __init__(self):
        """Инициализация объекта."""
        self.position_ = []

    def generate_random_position(self) -> list[int]:
        """
        Генерация случайный позиции для объекта.

        Returns:
            list[int]: случайные x и y на карте.
        """
        return [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        ]

    def draw(self):
        """Рендер объекта при помощи pygame."""
        pass


class Food(GameObject):
    """Базовые класс для еды."""

    # Съедобность еды,
    # Влияет на прибавление
    # или отнимание длины змейки.
    IS_EATABLE: bool

    # Цвет еды.
    COLOR: tuple

    # Сколько клеток изменияется
    # при съедании.
    CHANGE_CELLS: int

    def __init__(self):
        """Инициализация еды."""
        super().__init__()
        self.update_position()

    def update_position(self):
        """Смена позиции еды."""
        self.position_ = self.generate_random_position()

    def draw(self):
        """Рендер еды при помощи pygame."""
        rect = pygame.Rect(self.position_, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(Food):
    """
    Класс для яблок.
    Наследован от Food.
    """

    IS_EATABLE = True
    COLOR = APPLE_COLOR
    CHANGE_CELLS = 2


class Onion(Food):
    """
    Класс для чесноков.
    Наследован от Food.
    """

    IS_EATABLE = False
    COLOR = ONION_COLOR
    CHANGE_CELLS = 1


class Snake(GameObject):
    """Класс для змеек."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()

        self.position_.append(self.generate_random_position())
        self.direction = None
        self.next_direction = None
        self.change_tail = 0

    def move(self):
        """Обработка движения змейки."""
        handle_keys(self)

        if self.next_direction is None:
            return

        head_x, head_y = self.position_[0]
        move_x, move_y = self.next_direction

        head_x += move_x * GRID_SIZE
        head_y += move_y * GRID_SIZE

        if (
            head_x >= SCREEN_WIDTH
            or head_x < 0
            or head_y < 0
            or head_y >= SCREEN_HEIGHT
        ):
            self.__init__()
            return

        if self.change_tail > 0:
            for _ in range(self.change_tail):
                self.position_.append(self.position_[-1])
        if self.change_tail < 0:
            for _ in range(abs(self.change_tail)):
                self.position_.pop()

        if len(self.position_) == 0:
            self.__init__()
            return

        head = [head_x, head_y]
        if head in self.position_:
            self.__init__()
            return
        self.position_ = [head] + self.position_
        self.position_.pop()

        self.direction = self.next_direction
        self.change_tail = 0

    def try_eat(self, food: Food) -> bool:
        """
        Попытка скушать еду змейкой.

        Args:
            food (Food): любая еда.

        Returns:
            bool: была ли съедена еда.
        """
        if self.position_[0] == food.position_:
            if food.IS_EATABLE:
                self.change_tail = food.CHANGE_CELLS
            else:
                self.change_tail = -food.CHANGE_CELLS

            return True
        return False

    def draw(self):
        """Рендер змейки при помощи pygame."""
        for position in self.position_:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_small_snake(key, game_object: GameObject):
    """Обработка кнопок для маленького объекта.

    Args:
        key (_type_): кнопка, которая была нажата.
        game_object (GameObject): объект для обработки.
    """
    keys = (
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_LEFT,
        pygame.K_RIGHT,
    )

    if key in keys and len(game_object.position_) == 1:
        if key == pygame.K_UP:
            game_object.next_direction = UP
        elif key == pygame.K_DOWN:
            game_object.next_direction = DOWN
        elif key == pygame.K_LEFT:
            game_object.next_direction = LEFT
        elif key == pygame.K_RIGHT:
            game_object.next_direction = RIGHT


def handle_keys(game_object: GameObject):
    """
    Обработка кнопок и направление движения.

    Args:
        game_object (GameObject): игровой объект.

    Raises:
        SystemExit: пользователь хочет выйти.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            key = event.key

            if len(game_object.position_) == 1:
                handle_small_snake(key, game_object)
                return

            if key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif (
                key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Точка входа для программы."""
    pygame.init()

    snake = Snake()

    cnt_of_apples = 2
    cnt_of_onions = 1

    # Макс. кол-во еды, которую можно скушать,
    # после происходит перестановка еды на карте.
    max_eatable_cnt = None or 3

    current_eatable_cnt = 0

    foods = list()

    for _ in range(cnt_of_apples):
        foods.append(Apple())

    for _ in range(cnt_of_onions):
        foods.append(Onion())

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.move()

        for food in foods:
            if snake.try_eat(food):
                food.update_position()
                if max_eatable_cnt:
                    current_eatable_cnt += 1 if food.IS_EATABLE else 0

        if current_eatable_cnt >= max_eatable_cnt:
            for food in foods:
                food.update_position()

            current_eatable_cnt = 0

        snake.draw()

        for food in foods:
            food.draw()

        clock.tick(SPEED)

        pygame.display.flip()


if __name__ == "__main__":
    main()
