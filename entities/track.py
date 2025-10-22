# entities/track.py
import pygame

class Track:
    def __init__(self, image, screen_height, offset_x=0):
        self.image = image
        self.height = self.image.get_height()
        self.offset_x = offset_x  # Novo parâmetro para deslocamento
        self.y1 = 0
        self.y2 = -self.height
        self.speed = 5  # Velocidade da pista
        self.screen_height = screen_height
        self.frozen = False

    def update(self, dt):
        if not hasattr(self, 'frozen'):
            self.frozen = False
        if not self.frozen:
            # Velocidade base multiplicada por 60 para manter a mesma velocidade em 60 FPS
            speed_dt = self.speed * 60 * dt
            self.y1 += speed_dt
            self.y2 += speed_dt

            # Reseta as posições para loop da imagem
            if self.y1 >= self.screen_height:
                self.y1 = self.y2 - self.height
            if self.y2 >= self.screen_height:
                self.y2 = self.y1 - self.height

    def draw(self, surface):
        surface.blit(self.image, (self.offset_x, self.y1))
        surface.blit(self.image, (self.offset_x, self.y2))
