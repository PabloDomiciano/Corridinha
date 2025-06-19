import pygame
from entities.pickups.base_pickup import BasePickup
from entities.pickups.effects.ghost_effect import GhostPickupEffect

class GhostPickup(BasePickup):
    def __init__(self, image, x_pos, screen_height):
        super().__init__(image, x_pos, y_pos=0, speed=5)
        self.screen_height = screen_height

