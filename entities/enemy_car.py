# entities/enemy_car.py

from entities.base import BaseEntity

class EnemyCar(BaseEntity):
    def __init__(self, image, lane_x, screen_height):
        # Começa fora da tela (acima do topo)
        super().__init__(image, lane_x, -image.get_height())
        self.speed = 6
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
