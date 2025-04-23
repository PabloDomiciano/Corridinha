import pygame
import random

class FuelPickup:
    def __init__(self, image, height):
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([140, 280])
        self.rect.y = random.randint(-200, -50)
        self.speed = 5
        self.height = height

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > self.height
