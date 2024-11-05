import pygame, sys
from settings import WIDTH, HEIGHT, NAV_HEIGHT
from world import World

pygame.init()
screens = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("PacMan")

class Main:
    def __init__(self, screens):
        self.screens = screens
        self.FPS = pygame.time.Clock()
    def main(self):
        world = World(self.screens)
        while True:
            self.screens.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            world.update()
            pygame.display.update()
            self.FPS.tick(30)


if __name__ == "__main__":
    play = Main(screens)
    play.main()