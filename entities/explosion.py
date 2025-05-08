import pygame


class Explosion:
    def __init__(self, image, x, y, duration=500):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.start_time = pygame.time.get_ticks()
        self.duration = duration  # milissegundos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration
