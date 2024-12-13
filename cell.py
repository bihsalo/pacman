"""Модуль ячеек на игровом поле и их параметризации"""

import pygame


class Cell(pygame.sprite.Sprite):
    """
    Класс ячейки на игровом поле.

    Аргументы:
        width (int): Ширина ячейки.
        height (int): Высота ячейки.
        id (tuple): Координаты ячейки.
        abs_x (int): Координата X.
        abs_y (int): Координата Y.
        rect (pygame.Rect): Область ячейки.
        occupying_piece (None or object): Есть что-то в ячейке.
    """


    def __init__(self, row, col, length, width):
        """
        Объект Cell.

        Аргументы:
            row (int): Номер строки ячейки.
            col (int): Номер столбца ячейки.
            length (int): Ширина ячейки.
            width (int): Высота ячейки.
        """
        super().__init__()
        self.width = length
        self.height = width
        self.id = (row, col)
        self.abs_x = row * self.width
        self.abs_y = col * self.height
        self.rect = pygame.Rect(self.abs_x,self.abs_y,self.width,self.height)
        self.occupying_piece = None


    def update(self, screens):
        """
        Отображает ячейку на экране.

        Аргументы:
            screens (pygame.Surface): Поверхность, где рисуется ячейка.
        """
        pygame.draw.rect(screens, pygame.Color("blue2"), self.rect)