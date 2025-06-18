import pygame
import random
from core.game_world import GameWorld
from entities.pickups.effects.ghost_effect import GhostPickupEffect
from img.img_config import ImgConfig
from ui.hud import HUD
from ui.screen import Screen
from entities.pickups.ghost import GhostPickup



class GameManager:
    def __init__(self, width, height, title):
        pygame.init()

        # Configurações básicas
        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        
        # Sistemas principais
        self.screen = Screen(width, height, title)
        self.img_config = ImgConfig(self.width, self.height)
        self.game_world = GameWorld(width, height, self.img_config)
        self.hud = HUD(self.screen.surface, self.game_world.car)

        # Configuração do poder fantasma
        self._init_ghost_power_settings()

    def _init_ghost_power_settings(self):
        """Inicializa todas as configurações relacionadas ao poder fantasma."""
        self.ghost_effect = GhostPickupEffect(self.game_world.car)
        self.ghost_power = None
        self.ghost_power_active = False
        self.ghost_power_spawn_timer = pygame.time.get_ticks()
        self.ghost_power_spawn_interval = 5000  # 5 segundos entre spawns
        self.ghost_power_duration = 8000  # 8 segundos de duração
        self.blink_start_time = 3000  # Começa a piscar 3 segundos antes de acabar

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            self._handle_events()
            current_time = pygame.time.get_ticks()
            
            self._update_game_state(current_time)
            self._render_game()
            
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def _handle_events(self):
        """Lida com eventos de entrada."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update_game_state(self, current_time):
        """Atualiza todo o estado do jogo."""
        keys = pygame.key.get_pressed()
        self.game_world.update(keys)
        
        self._handle_ghost_power(current_time)
        self._check_game_conditions()

    def _handle_ghost_power(self, current_time):
        """Gerencia toda a lógica do poder fantasma."""
        self._spawn_ghost_power_if_needed(current_time)
        self._update_existing_ghost_power(current_time)
        self._update_ghost_effect(current_time)

    def _spawn_ghost_power_if_needed(self, current_time):
        """Verifica se precisa spawnar um novo poder fantasma."""
        if (not self.ghost_power_active and current_time - self.ghost_power_spawn_timer > self.ghost_power_spawn_interval and (self.ghost_power is None or self.ghost_power.off_screen(self.height))):
            self._spawn_ghost_power()
            self.ghost_power_spawn_timer = current_time


    def _spawn_ghost_power(self):
        """Cria um novo poder fantasma em uma pista aleatória."""
        if hasattr(self.game_world, 'road_lanes') and self.game_world.road_lanes:
            lane = random.choice(self.game_world.road_lanes)
        else:
            lane = random.randint(50, self.width - 50)

        self.ghost_power = GhostPickup(
            self.img_config.ghost_power_img,
            lane - self.img_config.ghost_power_img.get_width() // 2,
            -self.img_config.ghost_power_img.get_height(),
            self.img_config.ghost_power_img
        )

    def _update_existing_ghost_power(self, current_time):
        """Atualiza e verifica o poder fantasma existente."""
        if self.ghost_power is not None:
            self.ghost_power.update()
            
            if (self.ghost_power.check_collision(self.game_world.car) and
                not self.ghost_power.is_active() and
                not self.ghost_power_active):
                
                self._activate_ghost_power(current_time)

    def _activate_ghost_power(self, current_time):
        """Ativa o efeito do poder fantasma."""
        self.ghost_power.activate(current_time)
        self.ghost_effect.set_ghost_mode(True)
        self.ghost_power_active = True

    def _update_ghost_effect(self, current_time):
        """Atualiza o efeito visual do poder fantasma."""
        if not self.ghost_power_active or self.ghost_power is None:
            return

        remaining_time = self.ghost_power.get_remaining_time(current_time, self.ghost_power_duration)
        
        if remaining_time < self.blink_start_time:
            self.ghost_effect.is_blinking = True
            self.ghost_effect.update_blink(current_time)
        else:
            self.ghost_effect.is_blinking = False

        if remaining_time <= 0:
            self._deactivate_ghost_power()

    def _deactivate_ghost_power(self):
        """Desativa o poder fantasma."""
        self.ghost_effect.set_ghost_mode(False)
        self.ghost_power_active = False
        self.ghost_power = None

    def _check_game_conditions(self):
        """Verifica condições de fim de jogo."""
        self._check_collisions()
        self._check_fuel()

    def _check_collisions(self):
        """Verifica colisões com inimigos."""
        for enemy in self.game_world.enemies[:]:
            if self.ghost_effect.check_hitbox_collision(enemy):
                print("COLISÃO! FIM DE JOGO")
                self.running = False

    def _check_fuel(self):
        """Verifica se o combustível acabou."""
        if self.game_world.car.fuel <= 0:
            print("COMBUSTÍVEL ACABOU! FIM DE JOGO")
            self.running = False

    def _render_game(self):
        """Renderiza todos os elementos do jogo."""
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)
        self._draw_ghost_power()
        self.hud.update()
        self.hud.draw()

    def _draw_ghost_power(self):
        """Desenha o poder fantasma se estiver ativo e visível."""
        if (self.ghost_power is not None and
            not self.ghost_power.off_screen(self.height) and
            not self.ghost_power.is_active()):
            
            self.ghost_power.draw(self.screen.surface)