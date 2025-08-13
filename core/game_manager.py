import pygame
import sys
import random
from core.game_world import GameWorld
from entities.pickups.effects.ghost_effect import GhostPickupEffect
from img.img_config import ImgConfig
from ui.hud import HUD
from ui.screen import Screen

class SideGif:
    """GIF lateral que desce verticalmente, com tamanho customizável"""
    def __init__(self, frames, x, y, speed=5, frame_duration=300, size=None):
        """
        frames: lista de imagens do GIF
        x, y: posição inicial
        speed: velocidade vertical
        frame_duration: tempo (ms) entre frames
        size: tupla (largura, altura) opcional para redimensionar cada GIF
        """
        self.frames = frames
        if size:
            self.frames = [pygame.transform.scale(f, size) for f in frames]
        self.x = x
        self.y = y
        self.speed = speed
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.total_frames = len(self.frames)
        self.screen_height = pygame.display.get_surface().get_height()

    def update(self):
        now = pygame.time.get_ticks()
        if self.total_frames > 0 and now - self.last_update >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % self.total_frames
            self.last_update = now

        # Movimento vertical
        self.y += self.speed
        if self.y > self.screen_height:
            self.y = -50  # reinicia no topo

    def draw(self, surface):
        if self.total_frames > 0:
            surface.blit(self.frames[self.current_frame], (self.x, self.y))


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

        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.game_over_time = None

        self.hud = HUD(self.screen.surface, self.game_world.car, self.img_config, lambda: self.score)
        self.ghost_effect = GhostPickupEffect(self.game_world.car)
        self.player_controls_enabled = True
        self.showing_explosion = False
        self.explosion_end_time = 0

        # GIFs laterais
        self.side_gifs_list = []
        self._init_side_gifs()

    def _init_side_gifs(self):
        """Cria GIFs laterais com tamanho individual"""
        if not self.img_config.side_gifs:
            print("Nenhum GIF encontrado.")
            return

        sizes = {
            "coqueiro": (40, 80),    # tamanho específico para 'coqueiro'
            "default": (40, 40),     # tamanho padrão para outros GIFs
        }

        for folder_name, frames in self.img_config.side_gifs.items():
            if not frames:
                continue
            size = sizes.get(folder_name, sizes["default"])

            # Lado esquerdo
            x_left = 6
            y_left = random.randint(-200, self.height - 50)

            # Lado direito
            x_right = self.width - size[0] - 6
            y_right = random.randint(-200, self.height - 50)
            # evita que fiquem muito próximos verticalmente
            while abs(y_right - y_left) < 80:
                y_right = random.randint(-200, self.height - 50)

            self.side_gifs_list.append(SideGif(frames, x_left, y_left, speed=5, frame_duration=300, size=size))
            self.side_gifs_list.append(SideGif(frames, x_right, y_right, speed=5, frame_duration=300, size=size))

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
        if not self.game_over:
            self.score = (current_time - self.start_ticks) // 100

        keys = pygame.key.get_pressed() if self.player_controls_enabled else {}
        self.game_world.update(keys)
        self._handle_ghost_power(current_time)

        # Atualiza GIFs laterais
        for gif in self.side_gifs_list:
            gif.update()

        if not self.showing_explosion and not self.game_over:
            self._check_game_conditions()
        
        if self.game_over and current_time - self.game_over_time > 3000:
            self.running = False

        if self.showing_explosion and current_time >= self.explosion_end_time:
            self.running = False

    def _handle_ghost_power(self, current_time):
        for pickup in self.game_world.ghost_pickups[:]:
            if pickup.check_collision(self.game_world.car):
                self._activate_ghost_power(current_time)
                self.game_world.ghost_pickups.remove(pickup)
                break
        self._update_ghost_effect(current_time)

    def _activate_ghost_power(self, current_time):
        self.game_world.car.ghost_power_active = True
        self.game_world.car.ghost_power_end_time = current_time + 8000
        self.ghost_effect.set_ghost_mode(True)

    def _update_ghost_effect(self, current_time):
        if not self.game_world.car.ghost_power_active:
            return
        remaining = self.game_world.car.ghost_power_end_time - current_time
        if remaining < self.game_world.car.blink_start_offset:
            self.ghost_effect.is_blinking = True
            self.ghost_effect.update(current_time)
        else:
            self.ghost_effect.is_blinking = False
        if remaining <= 0:
            self._deactivate_ghost_power()

    def _deactivate_ghost_power(self):
        self.game_world.car.ghost_power_active = False
        self.ghost_effect.set_ghost_mode(False)

    def _check_game_conditions(self):
        self._check_collisions()
        self._check_fuel()

    def _check_collisions(self):
        if not self.game_world.enemies:
            return
        current_time = pygame.time.get_ticks()
        ghost_mode_active = getattr(self.game_world.car, 'ghost_power_active', False) and \
                            current_time < getattr(self.game_world.car, 'ghost_power_end_time', 0)
        for enemy in self.game_world.enemies[:]:
            if self.game_world.car.check_collision(enemy):
                if ghost_mode_active:
                    continue
                self.game_world.freeze_all()
                self.player_controls_enabled = False
                car_center = self.game_world.car.rect.center
                self.game_world.explosion.trigger(car_center[0], car_center[1], 50)
                self.explosion_end_time = current_time + 2000
                self.showing_explosion = True
                self.game_over = True
                self.game_over_time = current_time
                break

    def _check_fuel(self):
        if self.game_world.car.fuel <= 0:
            self.game_world.freeze_all()
            self.game_over = True
            self.game_over_time = pygame.time.get_ticks()

    def _render(self):
        self.screen.surface.fill((0, 0, 0))
        self.game_world.draw(self.screen.surface)

        # Desenha GIFs laterais
        for gif in self.side_gifs_list:
            gif.draw(self.screen.surface)

        # HUD
        self.hud.update()
        self.hud.draw()

        # Overlay final
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill((50, 50, 50))
            self.screen.surface.blit(overlay, (0, 0))

            font = pygame.font.Font(None, 50)
            final_text = font.render(f"Pontuação Final: {self.score}", True, (255, 255, 255))
            text_x = self.width // 2 - final_text.get_width() // 2
            text_y = self.height // 2 - final_text.get_height() // 2
            self.screen.surface.blit(final_text, (text_x, text_y))
