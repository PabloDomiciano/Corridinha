import pygame
from entities.base import BaseEntity
from entities.hitbox import Hitbox


class Carro(BaseEntity):
    def __init__(self, image, x_pos, y_pos, speed=0):
        super().__init__(image, x_pos, y_pos)
        self.speed = speed

        # Inicializa o retângulo e hitbox
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.init_hitbox()

    def init_hitbox(self):
        """Inicializa a hitbox do carro."""
        hitbox_width = self.rect.width
        hitbox_height = self.rect.height

        hitbox_x = self.rect.x + (self.rect.width - hitbox_width) / 2
        hitbox_y = self.rect.y + (self.rect.height - hitbox_height) / 2

        self.hitbox = Hitbox()
        self.hitbox.set_rect(hitbox_width, hitbox_height, hitbox_x, hitbox_y)

    def update(self):
        """Atualiza a hitbox com base na posição."""
        hitbox_x = self.rect.x + (self.rect.width - self.hitbox.rect.width) / 2
        hitbox_y = self.rect.y + (self.rect.height - self.hitbox.rect.height) / 2
        self.hitbox.set_rect(self.hitbox.rect.width, self.hitbox.rect.height, hitbox_x, hitbox_y)

    def draw(self, screen):
        """Desenha o carro."""
        screen.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(screen)

    def check_hitbox_collision(self, other):
        """Verifica colisão entre hitboxes."""
        return self.hitbox.check_rect_collision(other)

    def check_collision(self, other_car):
        """Verifica colisão simples com outro carro."""
        return self.rect.colliderect(other_car.rect)
