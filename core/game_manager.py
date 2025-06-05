import pygame
from core.game_world import GameWorld
from img.img_config import ImgConfig
from ui.hud import HUD

from ui.screen import Screen


class GameManager:
    def __init__(self, width, height, title):
        pygame.init()

        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)

        self.img_config = ImgConfig(self.width, self.height)
        self.game_world = GameWorld(width, height, self.img_config)
        self.hud = HUD(self.screen.surface, self.game_world.car)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(keys)
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def update(self, keys):
        self.game_world.update(keys)

        # Verifica colisões com inimigos
        for enemy in self.game_world.enemies[:]:
            if self.game_world.car.check_hitbox_collision(enemy):
                print("COLISÃO! FIM DE JOGO")
                self.running = False

        # Verifica se o jogo deve continuar (combustível, etc.)
        if self.game_world.car.fuel <= 0:
            print("COMBUSTÍVEL ACABOU! FIM DE JOGO")
            self.running = False

    def draw(self):
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()
