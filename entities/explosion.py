import pygame
from entities.effects.particula import Particle

class Explosion:
    def __init__(self, img_config):
        self.animation_frames = [
            pygame.transform.scale(img_config.explosion_1, (80, 80)),
            pygame.transform.scale(img_config.explosion_2, (120, 120)),
            pygame.transform.scale(img_config.explosion_3, (160, 160))
        ]
        self.current_frame = 0
        self.active = False
        self.position = (0, 0)
        self.animation_speed = 100  # ms entre frames
        self.last_update = 0

    def trigger(self, x, y, particle_count=30):
        self.active = True
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.position = (x, y)

    def update(self):
        if not self.active:
            return
            
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame += 1
            
            if self.current_frame >= len(self.animation_frames):
                self.active = False

    def draw(self, surface):
        if not self.active:
            return
            
        frame = self.animation_frames[self.current_frame]
        rect = frame.get_rect(center=self.position)
        surface.blit(frame, rect)