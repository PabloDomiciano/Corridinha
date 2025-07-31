import pygame
from core.game_world import GameWorld
from entities.pickups.effects.ghost_effect import GhostPickupEffect
from img.img_config import ImgConfig
from ui.hud import HUD
from ui.screen import Screen

class GameManager:
    def __init__(self, width, height, title):
        pygame.init()
<<<<<<< Updated upstream
        
=======

>>>>>>> Stashed changes
        # Configurações básicas
        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
<<<<<<< Updated upstream
        
=======

>>>>>>> Stashed changes
        # Sistemas principais
        self.screen = Screen(width, height, title)
        self.img_config = ImgConfig(width, height)
        self.game_world = GameWorld(width, height, self.img_config)
<<<<<<< Updated upstream
        self.hud = HUD(self.screen.surface, self.game_world.car)
        
=======
        self.hud = HUD(self.screen.surface, self.game_world.car, self.img_config)

>>>>>>> Stashed changes
        # Efeito ghost
        self.ghost_effect = GhostPickupEffect(self.game_world.car)
        self.ghost_power_active = False
        self.ghost_power_end_time = 0
        self.blink_start_offset = 3000  # 3 segundos antes do fim

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            current_time = pygame.time.get_ticks()
<<<<<<< Updated upstream
            
            self._handle_events()
            self._update(current_time)
            self._render()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
=======
            delta_time = self.clock.get_time() / 1000.0  # Em segundos

            self._handle_events()
            self._update(current_time, delta_time)
            self._render()

            pygame.display.flip()
            self.clock.tick(self.fps)

>>>>>>> Stashed changes
        pygame.quit()

    def _handle_events(self):
        """Lida com eventos de entrada."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

<<<<<<< Updated upstream
    def _update(self, current_time):
        """Atualiza o estado do jogo."""
        keys = pygame.key.get_pressed()
        self.game_world.update(keys)
        
=======
    def _update(self, current_time, delta_time):
        """Atualiza o estado do jogo."""
        keys = pygame.key.get_pressed()
        self.game_world.update(keys, delta_time)

>>>>>>> Stashed changes
        self._handle_ghost_power(current_time)
        self._check_game_conditions()

    def _handle_ghost_power(self, current_time):
        """Gerencia toda a lógica do poder fantasma."""
        self._check_ghost_pickup_collision(current_time)
        self._update_ghost_effect(current_time)

    def _check_ghost_pickup_collision(self, current_time):
        """Verifica colisão com pickups de ghost."""
        for pickup in self.game_world.ghost_pickups[:]:
            if pickup.check_collision(self.game_world.car):
                self._activate_ghost_power(current_time)
                self.game_world.ghost_pickups.remove(pickup)
                break

    def _activate_ghost_power(self, current_time):
        """Ativa o poder fantasma."""
        self.ghost_effect.set_ghost_mode(True)
        self.ghost_power_active = True
<<<<<<< Updated upstream
        self.ghost_power_end_time = current_time + 8000  # 8 segundos de duração
=======
        self.ghost_power_end_time = current_time + 8000  # 8 segundos
>>>>>>> Stashed changes

    def _update_ghost_effect(self, current_time):
        """Atualiza o efeito ghost."""
        if not self.ghost_power_active:
            return
<<<<<<< Updated upstream
            
        remaining_time = self.ghost_power_end_time - current_time
        
        # Ativa piscar quando faltar pouco tempo
=======

        remaining_time = self.ghost_power_end_time - current_time

>>>>>>> Stashed changes
        if remaining_time < self.blink_start_offset:
            self.ghost_effect.is_blinking = True
            self.ghost_effect.update_blink(current_time)
        else:
            self.ghost_effect.is_blinking = False
<<<<<<< Updated upstream
        
        # Desativa quando o tempo acabar
=======

>>>>>>> Stashed changes
        if remaining_time <= 0:
            self._deactivate_ghost_power()

    def _deactivate_ghost_power(self):
        """Desativa o poder fantasma."""
        self.ghost_effect.set_ghost_mode(False)
        self.ghost_power_active = False

    def _check_game_conditions(self):
        """Verifica condições de fim de jogo."""
        self._check_collisions()
        self._check_fuel()

    def _check_collisions(self):
        """Verifica colisões com inimigos."""
        for enemy in self.game_world.enemies[:]:
            if self.ghost_effect.check_collision(enemy):
                print("COLISÃO! FIM DE JOGO")
                self.running = False

    def _check_fuel(self):
        """Verifica se o combustível acabou."""
        if self.game_world.car.fuel <= 0:
            print("COMBUSTÍVEL ACABOU! FIM DE JOGO")
            self.running = False

    def _render(self):
        """Renderiza todos os elementos do jogo."""
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()