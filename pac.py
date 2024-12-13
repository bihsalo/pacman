"""Модуль с параметризацией пакмена"""

import pygame
from settings import CHAR_SIZE, PLAYER_SPEED
from animation import import_sprite


class Pac(pygame.sprite.Sprite):
    """
       Класс создающий пакмена

       аргументы:
           abs_x (int): расположение пакмена по оси x.
           abs_y (int): расположение пакмена по оси у.
           animations (dict): словарь, содержащий анимацию действий Pac-Man.
           frame_index (float): текущий индекс кадра для анимации.
           animation_speed (float): скорость перехода анимации.
           image (pygame.Surface): изобращение текущей анимации пакмена.
           rect (pygame.Rect): квадратик, определяющий положение и размер Pac-Man.
           mask (pygame.Mask): маска, используемая для точного обнаружения столкновений с объектов до пикселя.
           pac_speed (int): скорость пакмена.
           immune_time (int): время power_up облика с иммунитетом.
           immune (bool): проверка пакмена на иммунитет в данный момент.
           directions (dict): определение направлений движения (векторов).
           keys (dict): сопоставление направления пакмена привязкой к клавишам.
           direction (tuple): текущее направление пакмена.
           status (str): определение текущего статуса пакмена для анимации.
           life (int): кол-во оставшихся жизней у пакмена.
           pac_score (int): текущий счет пакмена
       """


    def __init__(self, row, col):
        """
        реализация спрайта пакмена

        Args:
            row (int): индексирование строки стартовой позиции пакмена.
            col (int): индексирование столбца стартовой позиции пакмена.
        """
        super().__init__()
        self.abs_x = (row * CHAR_SIZE)
        self.abs_y = (col * CHAR_SIZE)
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.4
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = (self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.pac_speed = PLAYER_SPEED
        self.immune_time = 0
        self.immune = False
        self.directions = {'left': (-PLAYER_SPEED, 0), 'right': (PLAYER_SPEED, 0), 'up': (0, -PLAYER_SPEED), 'down': (0, PLAYER_SPEED)}
        self.keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
        self.direction = (0, 0)
        self.status = "idle"
        self.life = 3
        self.pac_score = 0


    def _import_character_assets(self):
        """
                подгрузка и установка файловых ассетов из системной папки.
                """
        character_path = "assets/anime/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "idle": [],
            "power_up": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)


    def _is_collide(self, x, y):
        tmp_rect = self.rect.move(x, y)
        if tmp_rect.collidelist(self.walls_collide_list) == -1:
            return False
        return True


    def move_to_start_pos(self):
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y


    def animate(self, pressed_key, walls_collide_list):

        animation = self.animations.get(self.status, [])
        # проверка на существование кадров анимации.
        if not animation:
            print(f"No frames found for '{self.status}' animation.")  # Логируем проблему
            return

        # анимация продолжается только если есть кадры.
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # безопасный доступ к элементам списка.
        image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(image, (CHAR_SIZE, CHAR_SIZE))

        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(image, (CHAR_SIZE, CHAR_SIZE))
        self.walls_collide_list = walls_collide_list
        for key, key_value in self.keys.items():
            if pressed_key[key_value] and not self._is_collide(*self.directions[key]):
                self.direction = self.directions[key]
                self.status = key if not self.immune else "power_up"
                break
        if not self._is_collide(*self.direction):
            self.rect.move_ip(self.direction)
            self.status = self.status if not self.immune else "power_up"
        if self._is_collide(*self.direction):
            self.status = "idle" if not self.immune else "power_up"


    def update(self):
        self.immune = True if self.immune_time > 0 else False
        self.immune_time -= 1 if self.immune_time > 0 else 0
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))