import pygame

class Track:
    def __init__(self, image, height):
        self.image = image
        self.y = 0
        self.speed = 5
        self.height = height

    def update(self):
        self.y += self.speed
        if self.y >= self.height:
            self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (0, self.y - self.height))
        screen.blit(self.image, (0, self.y))
