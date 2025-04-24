import pygame
from entities.base_car import BaseCar


class Car(BaseCar):
    def __init__(self, image, width, height):
        center_x = width // 2
        bottom_y = height - 30
        super().__init__(image, x=center_x, y=0, speed=6)
        self.rect.centerx = center_x
        self.rect.bottom = bottom_y
        self.width = width

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.width:
            self.rect.x += self.speed
