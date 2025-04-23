import pygame
import random
import sys

from entities.image import Image

class EnemyCar(Image):
    def __init__(self):
        # Escolhe aleatoriamente uma imagem de carro inimigo
        self.image = random.choice(self.car_enemy)
        # Ajusta o tamanho do carro inimigo
        self.image = pygame.transform.scale(self.image, (120, 200))
        self.rect = self.image.get_rect()
        # Lado esquerdo ou direito mais centralizado
        self.rect.x = random.choice([100, 250])
        # Coloca o inimigo fora da tela, no topo
        self.rect.y = random.randint(-200, -50)
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT
