import pygame

from entities.hitbox import Hitbox


class FuelPickup:
    def __init__(self, image, x_pos, screen_height):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x_pos, 0))
        self.speed = 5
        self.screen_height = screen_height

        # Inicializando a hitbox para combustível
        self.hitbox = Hitbox()
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def update(self):
        # O combustível desce pela tela
        self.rect.y += self.speed
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def check_collision(self, player):
        # Verifica a colisão com a hitbox do jogador
        return self.hitbox.check_rect_collision(player)

    def off_screen(self, height):
        return self.rect.y > height

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(surface)  # Desenha a hitbox do combustível
