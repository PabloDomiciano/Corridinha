import pygame
from entities.base import BaseEntity

class Rocket(BaseEntity):
    def __init__(self, x, y, speed=10):
        super().__init__(None, x, y)
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 100, 0))  # Laranja flamejante
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = 1

    def update(self):
        self.rect.y -= self.speed  

    def draw(self, surface):
        surface.blit(self.image, self.rect)