import pygame, sys
from settings import WIDTH, HEIGHT, NAV_HEIGHT
from world import World

"""Основной модуль игры"""

pygame.init()
screens = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("Поставьте зачет")


class Main:
    """
    Основной класс игры.

    Аргументы:
        screens (pygame.Surface): Экран.
        FPS (pygame.time.Clock): Частота кадров.
    """


    def __init__(self, screens):
        """
        Инициализирует основной класс игры.

        Аргументы:
            screens (pygame.Surface): Экран.
        """
        self.screens = screens
        self.FPS = pygame.time.Clock()


    def main(self):
        """
        Запускает основной цикл.

        Обрабатывает события, обновляет состояние мира и перерисовывает экран.
        """
        world = World(self.screens)
        while True:
            self.screens.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            world.update()
            pygame.display.update()
            self.FPS.tick(60)


if __name__ == "__main__":
    play = Main(screens)
    play.main()