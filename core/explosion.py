import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Carrega imagem da explosão (exemplo)
        self.image = pygame.image.load("images/explosion.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Tempo da explosão antes de desaparecer
        self.life_time = 500  # 500ms
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.creation_time > self.life_time:
            self.kill()  # Remove a explosão após o tempo
