import pygame
from entities.base import BaseEntity
from entities.hitbox import Hitbox


class BasePickup(BaseEntity):
    def __init__(self, image, x_pos, y_pos, speed=150):
        """
        Base para pickups: define imagem, posição e velocidade de descida.
        :param image: imagem do pickup.
        :param x_pos: posição x inicial.
        :param y_pos: posição y inicial.
        :param speed: velocidade de movimento vertical (px/seg).
        """
        super().__init__(image, x_pos, y_pos)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.speed = speed
        self.hitbox = Hitbox()
<<<<<<< Updated upstream
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.set_rect(
            self.rect.width,
            self.rect.height,
            self.rect.x,
            self.rect.y
        )

    def update(self):
        """Movimento padrão: desce na tela"""
        self.rect.y += self.speed
        self.update_hitbox()

    def check_collision(self, player):
        """Verifica colisão via hitbox"""
        return self.hitbox.check_rect_collision(player)
=======
        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def update(self, delta_time):
        """Atualiza posição vertical com base no tempo e sincroniza hitbox."""
        self.rect.y += self.speed * delta_time
        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)
>>>>>>> Stashed changes

    def off_screen(self, screen_height):
        """Verifica se o pickup saiu da tela."""
        return self.rect.top > screen_height

    def check_collision(self, player):
        """Verifica colisão com o jogador usando hitbox."""
        return self.hitbox.check_rect_collision(player.hitbox)

    def draw(self, screen):
        """Desenha o pickup na tela e opcionalmente sua hitbox."""
        screen.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(screen)
