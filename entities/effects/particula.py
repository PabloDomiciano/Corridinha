import pygame
import random
import math

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = (
            random.randint(200, 255),  # Vermelho
            random.randint(50, 150),    # Verde
            0                           # Sem azul
        )
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 3)
        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed
        self.lifetime = random.randint(300, 800)
        self.alpha = 255

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 16
        self.alpha = max(0, int((self.lifetime / 800) * 255))
        return self.lifetime > 0

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))