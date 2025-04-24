import pygame
import random


class EnemyCar:
    def __init__(self, image, x, height):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(-200, -100)
        self.speed = random.randint(4, 7)
        self.height = height

        # Ajusta a hitbox dinamicamente com base no tipo de veículo
        if self.image.get_width() > 90:  # exemplo: ônibus ou ambulância
            self.hitbox = self.rect.inflate(-self.rect.width *
                                            0.2, -self.rect.height * 0.1)
        else:  # carros menores
            self.hitbox = self.rect.inflate(-self.rect.width *
                                            0.3, -self.rect.height * 0.2)

    def update(self):
        self.rect.y += self.speed
        self.hitbox.y = self.rect.y  # Atualiza a posição da hitbox com o movimento do carro
        self.hitbox.x = self.rect.x  # Atualiza a posição da hitbox com o movimento do carro

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # Descomente para ver a hitbox

    def off_screen(self):
        return self.rect.top > self.height

    def collide_with(self, other_rect):
        """Verifica se há colisão entre a hitbox do inimigo e outro retângulo (ex: carro do jogador)"""
        return self.hitbox.colliderect(other_rect)
