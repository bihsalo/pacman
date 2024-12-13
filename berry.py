import pygame
from settings import CHAR_SIZE, PLAYER_SPEED

"""Параметризация "вишенок" в игре"""


class Berry(pygame.sprite.Sprite):
    """
    Класс ягоды на игровом поле.

    Аргументы:
        power_up (bool): Является ли ягода усилением.
        size (int): Размер ягоды.
        color (pygame.Color): Цвет ягоды.
        thickness (int): Толщина обводки ягоды.
        abs_x (int): Абсолютная координата X ягоды.
        abs_y (int): Абсолютная координата Y ягоды.
        rect (pygame.Rect): Временный прямоугольник для проверки столкновений.
    """


    def __init__(self, row, col, size, is_power_up=False):
        """
        Объект Berry.

        Аргументы:
            row (int): Номер строки, где ягода.
            col (int): Номер столбца, где ягода.
            size (int): Размер ягоды.
            is_power_up (bool, optional): Является ли ягода усилением.
        """
        super().__init__()
        self.power_up = is_power_up
        self.size = size
        self.color = pygame.Color("violetred")
        self.thickness = size
        self.abs_x = (row * CHAR_SIZE) + (CHAR_SIZE // 2)
        self.abs_y = (col * CHAR_SIZE) + (CHAR_SIZE // 2)
        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.size * 2, self.size * 2)


    def update(self, screens):
        """
        Обновляет состояние ягоды и отображает её на экране.

        Аргументы:
            screens (pygame.Surface): Поверхность для ягоды.
        """
        self.rect = pygame.draw.circle(screens, self.color, (self.abs_x, self.abs_y), self.size, self.thickness)