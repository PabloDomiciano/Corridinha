import pygame


class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # tamanho do projétil
        self.image.fill((255, 0, 0))  # cor vermelha
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = -10  # vai pra cima
     def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()  # remove quando sai da tela