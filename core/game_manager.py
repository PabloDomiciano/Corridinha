import pygame
from core.game_world import GameWorld
from entities.pickups.effects.ghost_effect import GhostPickupEffect
from entities.player import Player
from img import img_config
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
        self.img_config = ImgConfig(width, height)
        self.game_world = GameWorld(width, height, self.img_config)

        self.hud = HUD(self.screen.surface, self.game_world.car, self.img_config)

        self.ghost_effect = GhostPickupEffect(self.game_world.car)
        
        self.player_controls_enabled = True
        self.showing_explosion = False
        self.explosion_end_time = 0
        

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            self._handle_events()
            self._update(current_time)
            self._render()           
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def _update(self, current_time):
        keys = pygame.key.get_pressed() if self.player_controls_enabled else {}
        
        # Atualiza o mundo do jogo (que agora respeita o estado frozen)
        self.game_world.update(keys)
        
        # Atualiza efeitos do ghost
        self._handle_ghost_power(current_time)
        
        # Verifica condições do jogo
        if not self.showing_explosion:  # Só verifica colisões se não estiver em explosão
            self._check_game_conditions()
        
        # Finaliza o jogo após a explosão
        if self.showing_explosion and current_time >= self.explosion_end_time:
            self.running = False

    def _handle_ghost_power(self, current_time):
        self._check_ghost_pickup_collision(current_time)
        self._update_ghost_effect(current_time)

    def _check_ghost_pickup_collision(self, current_time):
        for pickup in self.game_world.ghost_pickups[:]:
            if pickup.check_collision(self.game_world.car):
                self._activate_ghost_power(current_time)
                self.game_world.ghost_pickups.remove(pickup)
                break

    def _activate_ghost_power(self, current_time):
        """Ativa o poder fantasma no jogador"""
        self.game_world.car.ghost_power_active = True
        self.game_world.car.ghost_power_end_time = current_time + 8000  # 8 segundos
        self.ghost_effect.set_ghost_mode(True)
    
    def _update_ghost_effect(self, current_time):
        """Atualiza o efeito fantasma"""
        if not self.game_world.car.ghost_power_active:
            return
            
        remaining_time = self.game_world.car.ghost_power_end_time - current_time
            
        # Ativa piscar nos últimos 3 segundos
        if remaining_time < self.game_world.car.blink_start_offset:
            self.ghost_effect.is_blinking = True
            self.ghost_effect.update(current_time)
        else:
            self.ghost_effect.is_blinking = False
                
        # Desativa quando o tempo acabar
        if remaining_time <= 0:
            self._deactivate_ghost_power()

    def _deactivate_ghost_power(self):
        """Desativa o poder fantasma"""
        self.game_world.car.ghost_power_active = False
        self.ghost_effect.set_ghost_mode(False)

    def _check_game_conditions(self):
        self._check_collisions()
        self._check_fuel()
        
        
    def _check_collisions(self):
        # Se não há inimigos, não precisa verificar colisões
        if not self.game_world.enemies:
            return
            
        # Verifica se o efeito fantasma está ativo no jogador
        current_time = pygame.time.get_ticks()
        ghost_mode_active = (hasattr(self.game_world.car, 'ghost_power_active') and 
                            self.game_world.car.ghost_power_active and 
                            current_time < self.game_world.car.ghost_power_end_time)

        for enemy in self.game_world.enemies[:]:
            if self.game_world.car.check_collision(enemy):
                if ghost_mode_active:
                    continue
                    
                # Verificação de segurança
                if not hasattr(self.game_world, 'frozen'):
                    self.game_world.frozen = False
                    
                # Congela todo o jogo
                self.game_world.freeze_all()
                self.player_controls_enabled = False

                # Ativa explosão
                car_center = self.game_world.car.rect.center
                self.game_world.explosion.trigger(car_center[0], car_center[1], 50)
                self.explosion_end_time = current_time + 2000
                self.showing_explosion = True
                break  # Sai do loop após a primeira colisão

    def _check_fuel(self):
        if self.game_world.car.fuel <= 0:
            print("COMBUSTÍVEL ACABOU! FIM DE JOGO")
            self.running = False

    def _render(self):
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()
