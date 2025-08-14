import random
import pygame


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
