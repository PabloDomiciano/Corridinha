import pygame
from entities.base import BaseEntity

class Rocket(BaseEntity):
    def __init__(self, x, y, speed=10):
        # Cria uma imagem padrão para o foguete
        image = pygame.Surface((20, 40), pygame.SRCALPHA)
        # Desenha um foguete simples
        pygame.draw.polygon(image, (255, 100, 0), [(10, 0), (20, 40), (0, 40)])
        pygame.draw.rect(image, (200, 200, 200), (8, 35, 4, 5))
        
        super().__init__(image, x, y)
        self.speed = speed
        self.damage = 1

    def update(self):
        if not self.frozen:
            self.rect.y -= self.speed