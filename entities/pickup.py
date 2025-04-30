import pygame

class Pickup:
    def __init__(self, image, lane, height):
        self.image = image
        self.lane = lane
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = self.lane
        self.rect.y = -self.rect.height  # Inicia fora da tela

    def update(self):
        """Move o pickup para baixo na tela."""
        self.rect.y += 5
        if self.rect.y > self.height:
            self.off_screen()

    def off_screen(self):
        """Verifica se o pickup saiu da tela e deve ser removido."""
        return self.rect.y > self.height

    def check_collision(self, car):
        """Verifica se o pickup colidiu com o carro do jogador."""
        return self.rect.colliderect(car.rect)

    def draw(self, surface):
        """Desenha o pickup na tela."""
        surface.blit(self.image, self.rect)
