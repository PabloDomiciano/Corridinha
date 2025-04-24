import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))  # cor vermelha
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = -10

    def update(self):
        self.rect.y += self.velocity
        if self.rect.bottom < 0:
            self.kill()
