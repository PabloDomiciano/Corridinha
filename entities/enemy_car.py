import pygame
from entities.carro import Carro


class EnemyCar(Carro):
    def __init__(self, image, x_pos, screen_height):
        super().__init__(image, x_pos, y_pos=-image.get_height())
        self.screen_height = screen_height
<<<<<<< Updated upstream

        # Inicializa a hitbox para o inimigo com a mesma posição e dimensões do carro
        self.hitbox = Hitbox()
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def update(self):
        # Atualiza a posição do carro inimigo
        self.rect.y += self.speed
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)
=======
        self.speed = 180  # velocidade em pixels por segundo

    def update(self, delta_time):
        """Atualiza a posição vertical com base no tempo."""
        self.rect.y += self.speed * delta_time
        self.update_hitbox()
>>>>>>> Stashed changes

    def off_screen(self, height):
        """Verifica se o inimigo saiu da tela."""
        return self.rect.top > height

    def draw(self, screen):
        """Desenha o carro inimigo."""
        super().draw(screen)

    def update_hitbox(self):
        """Atualiza a posição da hitbox."""
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y
        )
