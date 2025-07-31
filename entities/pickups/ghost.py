from entities.pickups.base_pickup import BasePickup
from entities.pickups.effects.ghost_effect import GhostPickupEffect


class GhostPickup(BasePickup):
    def __init__(self, image, x_pos, screen_height):
        # Define a posição inicial acima da tela e herda velocidade padrão (150)
        super().__init__(image, x_pos, y_pos=-image.get_height(), speed=150)
        self.screen_height = screen_height
