from entities.pickups.base_pickup import BasePickup


class SpeedBoostPickup(BasePickup):
    def __init__(self, image, x_pos, screen_height):
        # Spawna acima da tela e desce com velocidade padrão
        super().__init__(image, x_pos, y_pos=-image.get_height(), speed=150)
        self.screen_height = screen_height
