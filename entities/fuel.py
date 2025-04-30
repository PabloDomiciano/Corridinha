# entities/fuel.py

from entities.base import BaseEntity

class FuelPickup(BaseEntity):
    def __init__(self, image, lane_x, screen_height):
        super().__init__(image, lane_x, -image.get_height())
        self.speed = 4
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
