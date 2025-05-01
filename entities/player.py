from entities.car import Car


class Player(Car):
    
    def __init__(self, image, screen_width, screen_height, x_pos, y_pos):
        super().__init__(image, screen_width, screen_height, x_pos, y_pos)

    def update(self, keys):
        """Atualiza a posição do jogador com base nas teclas pressionadas."""
        super().update(keys)
