import pygame
from entities.carro import Carro
from entities.hitbox import Hitbox  # Não se esqueça de importar a classe Hitbox


class EnemyCar(Carro):
    def __init__(self, image, x_pos, screen_height, speed=3):
        super().__init__(image, x_pos, y_pos=-image.get_height(), speed=speed)
        self.screen_height = screen_height

        # Inicializa a hitbox para o inimigo com a mesma posição e dimensões do carro
        self.hitbox = Hitbox()
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def update(self):
        # Atualiza a posição do carro inimigo
        self.rect.y += self.speed
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def off_screen(self, height):
        return self.rect.y > height

    def draw(self, surface):
        # Desenha o carro inimigo e sua hitbox
        surface.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(surface)  # Desenha a hitbox do carro inimigo
