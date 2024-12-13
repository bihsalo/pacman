"""Модуль параметризации призраков в игре"""

import pygame
import random
import time
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED



class Ghost(pygame.sprite.Sprite):
    """
    Класс призрака.

    Аргументы:
        abs_x (int): Начальная координата Х.
        abs_y (int): Начальная координата Y.
        rect (pygame.Rect): Положение и размеры призрака.
        move_speed (int): Скорость призрака.
        color (pygame.Color): Цвет призрака.
        move_directions (list): Направления движения.
        moving_dir (str): Текущее направление движения.
        img_path (str): Путь к папке с изображениями призрака.
        img_name (str): Имя файла изображения текущего направления движения.
        image (pygame.Surface): Текущее изображение призрака.
        mask (pygame.Mask): Маска призрака для проверки столкновений.
        directions (dict): Словарь с направлениями движения и их смещениями.
        keys (list): Названия направлений.
        direction (tuple): Текущее смещение по X и Y.
    """


    def __init__(self, row, col, color):
        """
        Объект призрака.

        Аргументы:
            row (int): Начальная строка.
            col (int): Начальный столбец.
            color (str): Цвет призрака.
        """
        super().__init__()
        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)
        self.rect = pygame.Rect(self.abs_x, self.abs_y, CHAR_SIZE, CHAR_SIZE)
        self.move_speed = GHOST_SPEED
        self.color = pygame.Color(color)
        self.move_directions = [(-1,0), (0,-1), (1,0), (0,1)]
        self.moving_dir = "up"
        self.img_path = f'assets/ghosts/{color}/'
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft = (self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.directions = {'left': (-self.move_speed, 0), 'right': (self.move_speed, 0), 'up': (0, -self.move_speed), 'down': (0, self.move_speed)}
        self.keys = ['left', 'right', 'up', 'down']
        self.direction = (0, 0)


    def move_to_start_pos(self):
        """
        Перемещает призрака в начальную позицию.
        """
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y


    def is_collide(self, x, y, walls_collide_list):
        """
        Проверяет, сталкивается ли призрак с препятствием.

        Аргументы:
            x (int): Смещение по X.
            y (int): Смещение по Y.
            walls_collide_list (list): Список препятствий.

        Возвращает:
            bool: True - столкновение, иначе False.
        """
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
        return True


    def _animate(self):
        """
        Обновляет изображение призрака в соответствии с текущим направлением движения.
        """
        self.img_name = f'{self.moving_dir}.png'
        self.image = pygame.image.load(self.img_path + self.img_name)
        self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


    def update(self, walls_collide_list):
        """
        Состояние и движение призрака.

        Аргументы:
            walls_collide_list (list): Список препятствий.
        """
        available_moves = []
        for key in self.keys:
            if not self.is_collide(*self.directions[key], walls_collide_list):
                available_moves.append(key)
        randomizing = False if len(available_moves) <= 2 and self.direction != (0, 0) else True
        if randomizing and random.randrange(0, 100) <= 60:
            self.moving_dir = random.choice(available_moves)
            self.direction = self.directions[self.moving_dir]
        if not self.is_collide(*self.direction, walls_collide_list):
            self.rect.move_ip(self.direction)
        else:
            self.direction = (0, 0)
        if self.rect.right <= 0:
            self.rect.x = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.x = 0
        self._animate()