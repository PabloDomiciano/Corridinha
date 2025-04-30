import pygame
from abc import ABC, abstractmethod

class BaseEntity(ABC):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    @abstractmethod
    def update(self):
        """Atualização obrigatória para cada entidade específica."""
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def off_screen(self, screen_height):
        """Verifica se o objeto saiu da tela (parte inferior)."""
        return self.rect.top > screen_height

    def check_collision(self, other):
        """Verifica colisão com outra entidade."""
        return self.rect.colliderect(other.rect)
