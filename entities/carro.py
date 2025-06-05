import pygame
from entities.base import BaseEntity
from entities.hitbox import Hitbox


class Carro(BaseEntity):
    def __init__(self, image, x_pos, y_pos, speed=3):
        super().__init__(image, x_pos, y_pos)
        self.speed = speed

        # Inicializa o retângulo para a imagem do carro
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

        # Inicializa a hitbox com um tamanho diferente da imagem do carro
        hitbox_width = self.rect.width * 0.8  # 80% do tamanho da largura da imagem
        hitbox_height = self.rect.height * 0.100  # 60% da altura da imagem
        
        
        hitbox_x = self.rect.x + (self.rect.width - hitbox_width) / 2  # Centraliza a hitbox
        hitbox_y = self.rect.y + (self.rect.height - hitbox_height) / 2  # Centraliza a hitbox

        # Define a hitbox com o novo tamanho
        self.hitbox = Hitbox()
        self.hitbox.set_rect(hitbox_width, hitbox_height, hitbox_x, hitbox_y)
    def update(self):
        pass

    def draw(self, screen):
        # Desenha o carro e a hitbox
        screen.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(screen)

    def check_hitbox_collision(self, other):
        # Verifica a colisão entre a hitbox deste carro e a de outro objeto
        return self.hitbox.check_rect_collision(other)
