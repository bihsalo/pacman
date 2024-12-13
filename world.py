"""Модуль параметризации карты и игрового мира"""

import pygame
import time
from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP, PLAYER_SPEED
from pac import Pac
from cell import Cell
from berry import Berry
from ghost import Ghost
from display import Display


class World:


    """
    Отрисовка игрового поля.

    Аргументы:
        screens (pygame.Surface): Экран.
        player (pygame.sprite.GroupSingle): Характеристики пакмена.
        ghosts (pygame.sprite.Group): Характеристики призраков.
        walls (pygame.sprite.Group): Скелет стен.
        berries (pygame.sprite.Group): Скелет ягод.
        display (Display): Интерфейс.
        game_over (bool): Закончина ли игра.
        reset_pos (bool): Координаты точек респавна.
        player_score (int): Счет игрока.
        game_level (int): Текущий уровень.
    """


    def __init__(self, screens):


        """
        Объект игрового поля.

        Аргументы:
            screens (pygame.Surface): Экран.
        """
        self.screens = screens
        self.player = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.berries = pygame.sprite.Group()
        self.display = Display(self.screens)
        self.game_over = False
        self.reset_pos = False
        self.player_score = 0
        self.game_level = 1
        self._generate_world()


    def _generate_world(self):


        """
        Начальное состояние игрового поля.
        Заполняет поле стенами, ягодами, призраками и устанавливает начальную позицию пакмена.
        """
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == "1":
                    self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
                elif char == " ":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
                elif char == "p":
                    self.ghosts.add(Ghost(x_index, y_index, "pink"))
                elif char == "r":
                    self.ghosts.add(Ghost(x_index, y_index, "red"))

                elif char == "P":
                    self.player.add(Pac(x_index, y_index))

        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]


    def generate_new_level(self):


        """
        Заново заселяет игровое поле ягодами.
        """
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == " ":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
        time.sleep(2)


    def restart_level(self):


        """
        Перезапускает уровень, сбрасывая все сущности.
        """
        self.berries.empty()
        [ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
        self.game_level = 1
        self.player.sprite.pac_score = 0
        self.player.sprite.life = 3
        self.player.sprite.move_to_start_pos()
        self.player.sprite.direction = (0, 0)
        self.player.sprite.status = "idle"
        self.generate_new_level()


    def _dashboard(self):


        """
        Отображает игровую панель.
        """
        nav = pygame.Rect(0, HEIGHT, WIDTH, NAV_HEIGHT)
        pygame.draw.rect(self.screens, pygame.Color("cornsilk4"), nav)

        self.display.show_life(self.player.sprite.life)
        self.display.show_level(self.game_level)
        self.display.show_score(self.player.sprite.pac_score)


    def _check_game_state(self):


        """
        Проверяет текущее состояние игры.
        """
        if self.player.sprite.life == 0:
            self.game_over = True
        if len(self.berries) == 0 and self.player.sprite.life > 0:
            self.game_level += 1
            for ghost in self.ghosts.sprites():
                ghost.move_speed += self.game_level
                ghost.move_to_start_pos()
            self.player.sprite.move_to_start_pos()
            self.player.sprite.direction = (0, 0)
            self.player.sprite.status = "idle"
            self.generate_new_level()


    def update(self):


        """
        Обновляет состояние игры.
        Условия окончания игры и переходы между уровнями.
        """
        if not self.game_over:
            pressed_key = pygame.key.get_pressed()

            if self.player.sprite:
                self.player.sprite.animate(pressed_key, self.walls_collide_list)
            else:
                print("Пакмен не отрисован")

            if self.player.sprite.rect.right <= 0:
                self.player.sprite.rect.x = WIDTH
            elif self.player.sprite.rect.left >= WIDTH:
                self.player.sprite.rect.x = 0
            for berry in self.berries.sprites():
                if self.player.sprite.rect.colliderect(berry.rect):
                    if berry.power_up:
                        self.player.sprite.immune_time = 150
                        self.player.sprite.pac_score += 50
                    else:
                        self.player.sprite.pac_score += 10
                    berry.kill()
            for ghost in self.ghosts.sprites():
                if self.player.sprite.rect.colliderect(ghost.rect):
                    if not self.player.sprite.immune:
                        time.sleep(2)
                        self.player.sprite.life -= 1
                        self.reset_pos = True
                        break
                    else:
                        ghost.move_to_start_pos()
                        self.player.sprite.pac_score += 100
        self._check_game_state()
        [wall.update(self.screens) for wall in self.walls.sprites()]
        [berry.update(self.screens) for berry in self.berries.sprites()]
        [ghost.update(self.walls_collide_list) for ghost in self.ghosts.sprites()]
        self.ghosts.draw(self.screens)
        self.player.update()
        self.player.draw(self.screens)
        self.display.game_over() if self.game_over else None
        self._dashboard()
        if self.reset_pos and not self.game_over:
            [ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
            self.player.sprite.move_to_start_pos()
            self.player.sprite.status = "idle"
            self.player.sprite.direction = (0, 0)
            self.reset_pos = False
        if self.game_over:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_r]:
                self.game_over = False
                self.restart_level()


def animate(self, pressed_key, walls_collide_list):


    """
    Анимация игрока от ввода с клавиатуры.

    Аргументы:
        pressed_key (list): Нажатые клавиши.
        walls_collide_list (list): Cntys для проверки cтолкновений
    """
    animation = self.animations[self.status]

    print(f"Текуший статус: {self.status}")

    if not animation:
        return

    self.frame_index += self.animation_speed
    if self.frame_index >= len(animation):
        self.frame_index = 0

    image = animation[int(self.frame_index)]
    self.image = pygame.transform.scale(image, (CHAR_SIZE, CHAR_SIZE))