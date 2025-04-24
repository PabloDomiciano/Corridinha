import pygame

class GameObject:
    def __init__(self, image, x, y, speed=0, height=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.height = height

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.height is not None and self.rect.top > self.height

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)