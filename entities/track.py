# entities/track.py

import pygame

class Track:
    def __init__(self, image, screen_height):
        self.image = image
        self.height = self.image.get_height()
        self.y1 = 0
        self.y2 = -self.height
        self.speed = 5  # Velocidade da pista

        self.screen_height = screen_height

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed

        # Reseta as posições para loop da imagem
        if self.y1 >= self.screen_height:
            self.y1 = self.y2 - self.height
        if self.y2 >= self.screen_height:
            self.y2 = self.y1 - self.height

    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))
