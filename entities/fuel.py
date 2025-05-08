from entities.base import BaseEntity
import pygame


class FuelPickup(BaseEntity):
    def __init__(self, image, x_pos, screen_height, speed=3):
        super().__init__(image, x_pos, y_pos=-image.get_height())
        self.speed = speed
        self.screen_height = screen_height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed

    def check_collision(self, player):
        offset = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        return self.mask.overlap(player.mask, offset) is not None

    def off_screen(self, height):
        return self.rect.y > height
