import pygame
from core.game_world import GameWorld
from img.img_config import ImgConfig
from ui.hud import HUD
from ui.screen import Screen
from ui.start_screen import StartScreen
from ui.restart_screen import RestartScreen

class GameManager:
    def __init__(self, width, height, title):
        pygame.init()

        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)

        self.first_run = True  # Controla se deve mostrar a tela inicial
        self.font = pygame.font.Font(None, 36)

    def run(self):
        while self.running:
            if self.first_run:
                start_screen = StartScreen(self.screen.surface, self.font)
                acao = start_screen.mostrar_tela()
                if acao == "sair":
                    self.running = False
                    break
                self.first_run = False

            self.setup_jogo()
            resultado = self.loop_jogo()

            if resultado == "fim":
                restart_screen = RestartScreen(self.screen.surface, self.font)
                acao = restart_screen.mostrar_tela()
                if acao == "quit":
                    self.running = False
                # Se "restart", o loop volta e inicia o jogo sem passar pela start_screen

        pygame.quit()

    def setup_jogo(self):
        self.img_config = ImgConfig(self.width, self.height)
        self.game_world = GameWorld(self.width, self.height, self.img_config)
        self.hud = HUD(self.screen.surface, self.game_world.car)

    def loop_jogo(self):
        rodando = True
        while rodando:
            self.clock.tick(self.fps)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "fim"

            self.update(keys)
            self.draw()
            pygame.display.flip()

            if self.game_world.car.fuel <= 0:
                print("COMBUSTÍVEL ACABOU! FIM DE JOGO")
                return "fim"

            for enemy in self.game_world.enemies[:]:
                if self.game_world.car.check_hitbox_collision(enemy):
                    print("COLISÃO! FIM DE JOGO")
                    return "fim"

        return "fim"

    def update(self, keys):
        self.game_world.update(keys)

    def draw(self):
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()
