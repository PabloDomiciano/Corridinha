from entities.game_object import GameObject

class BaseCar(GameObject):
    def __init__(self, image, x=0, y=0, speed=5, height=None):
        super().__init__(image, x, y, speed, height)
