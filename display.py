import pygame
from settings import WIDTH, HEIGHT, CHAR_SIZE

"""Объектная и текстовая составляющая игры"""

pygame.font.init()


class Display:
    """
    Класс, отображения элементов: очки, уровень, жизни и завершение игры.

    Аргументы:
        screens (pygame.Surface): Экран.
        font (pygame.font.Font): Шрифт уровня и очков.
        game_over_font (pygame.font.Font): Шрифт завершения игры.
        text_color (pygame.Color): Цвет текста.
    """


    def __init__(self, screens):
        """
        Объект Display.

        Аргументы:
            screens (pygame.Surface): Поверхность экрана.
        """
        self.screens = screens
        self.font = pygame.font.SysFont("ubuntumono", CHAR_SIZE)
        self.game_over_font = pygame.font.SysFont("dejavusansmono", 48)
        self.text_color = pygame.Color("crimson")


    def show_life(self, life):
        """
        Кол-во жизней.

        Аргументы:
            life (int): Кол-во жизней.
        """
        img_path = "assets/life/life.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (CHAR_SIZE, CHAR_SIZE))
        life_x = CHAR_SIZE // 2
        if life != 0:
            for life in range(life):
                self.screens.blit(life_image, (life_x, HEIGHT + (CHAR_SIZE // 2)))
                life_x += CHAR_SIZE


    def show_level(self, level):
        """
        Текущий уровень.

        Аргументы:
            level (int): Номер текущего уровня.
        """
        level_x = WIDTH // 3
        level = self.font.render(f'Level {level}', True, self.text_color)
        self.screens.blit(level, (level_x, (HEIGHT + (CHAR_SIZE // 2))))


    def show_score(self, score):
        """
        Текущий счет.

        Аргументы:
            score (int): Текущий счет.
        """
        score_x = WIDTH // 3
        score = self.font.render(f'{score}', True, self.text_color)
        self.screens.blit(score, (score_x * 2, (HEIGHT + (CHAR_SIZE // 2))))


    def game_over(self):
        """
        Cообщение о завершении игры.
        """
        message = self.game_over_font.render(f'ИГРА ОКОНЧЕНА!', True, pygame.Color("chartreuse"))
        instruction = self.font.render(f'поставьте 10 для рестарта', True, pygame.Color("chartreuse"))
        self.screens.blit(message, ((WIDTH // 5.65), (HEIGHT // 3)))
        self.screens.blit(instruction, ((WIDTH // 3.76), (HEIGHT // 2)))