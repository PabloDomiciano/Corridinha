import pygame
import random
from core.game_world import GameWorld
from img.img_config import ImgConfig
from ui.hud import HUD
from ui.screen import Screen
from entities.ghost import GhostPowerPickup


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

        # Configuração do poder fantasma
        self.ghost_power = None
        self.ghost_power_active = False
        self.ghost_power_spawn_timer = pygame.time.get_ticks()
        self.ghost_power_spawn_interval = 5000  # 20 segundos entre spawns
        self.blink_start_time = 3000  # Começa a piscar 3 segundos antes de acabar

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(current_time, keys)
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def update(self, current_time, keys):
        # Atualiza o mundo do jogo
        self.game_world.update(keys)

        # Lógica de spawn do poder fantasma
        if (not self.ghost_power_active and
            current_time - self.ghost_power_spawn_timer > self.ghost_power_spawn_interval and
                (self.ghost_power is None or self.ghost_power.off_screen(self.height))):
            self.spawn_ghost_power()
            self.ghost_power_spawn_timer = current_time

        # Atualiza e verifica o poder fantasma
        if self.ghost_power is not None:
            self.ghost_power.update()

            # Verifica colisão com o jogador
            if (self.ghost_power.check_collision(self.game_world.car) and
                not self.ghost_power.is_active() and
                    not self.ghost_power_active):
                self.activate_ghost_power(current_time)

        # Controla o efeito de piscar quando o poder está acabando
        if self.ghost_power_active and self.ghost_power is not None:
            remaining_time = self.ghost_power.get_remaining_time()

            if remaining_time < self.blink_start_time:
                self.game_world.car.is_blinking = True
                self.game_world.car.update_blink(current_time)
            else:
                self.game_world.car.is_blinking = False

            # Verifica se o poder acabou
            if remaining_time <= 0:
                self.deactivate_ghost_power()

        # Verifica colisões com inimigos
        self.check_collisions()

        # Verifica combustível
        if self.game_world.car.fuel <= 0:
            print("COMBUSTÍVEL ACABOU! FIM DE JOGO")
            self.running = False

    def activate_ghost_power(self, current_time):
        """Ativa o poder fantasma."""
        self.ghost_power.activate(current_time)
        self.game_world.car.set_ghost_mode(True)
        self.ghost_power_active = True

    def deactivate_ghost_power(self):
        """Desativa o poder fantasma."""
        self.game_world.car.set_ghost_mode(False)
        self.ghost_power_active = False
        self.ghost_power = None

    def check_collisions(self):
        """Verifica colisões com carros inimigos."""
        for enemy in self.game_world.enemies[:]:
            if self.game_world.car.check_hitbox_collision(enemy):
                print("COLISÃO! FIM DE JOGO")
                self.running = False

    def spawn_ghost_power(self):
        """Spawna um novo poder fantasma em uma pista aleatória."""
        if hasattr(self.game_world, 'road_lanes') and self.game_world.road_lanes:
            lane = random.choice(self.game_world.road_lanes)
        else:
            lane = random.randint(50, self.width - 50)

        ghost_power_img = self.img_config.get_ghost_power_image()
        ghost_icon_img = self.img_config.get_ghost_icon_image()

        self.ghost_power = GhostPowerPickup(
            ghost_power_img,
            lane - ghost_power_img.get_width() // 2,
            self.height,
            ghost_icon_img
        )
        self.ghost_power.rect.y = -self.ghost_power.rect.height

    def draw(self):
        """Renderiza todos os elementos do jogo."""
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)

        # Desenha o poder fantasma se estiver no mundo
        if (self.ghost_power is not None and
            not self.ghost_power.off_screen(self.height) and
                not self.ghost_power.is_active()):
            self.ghost_power.draw(self.screen.surface)

        self.hud.update()
        self.hud.draw()
