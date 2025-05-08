import math
import pygame
from entities.base import BaseEntity


class Carro(BaseEntity):
    def __init__(self, image, x_pos, y_pos, speed=3):
        super().__init__(image, x_pos, y_pos)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = self.image.get_width() // 2

    def update(self):
        pass

    def check_mask_collision(self, other):
        offset = (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
        return self.mask.overlap(other.mask, offset) is not None

    def check_circle_collision(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        distance = math.hypot(dx, dy)
        return distance < self.radius + other.radius
