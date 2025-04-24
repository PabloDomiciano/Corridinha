import random
from entities.game_object import GameObject
from img.img_config import ImgConfig

class FuelPickup(GameObject):
    def __init__(self, image, height):
        self.image = image
        x = random.choice([140, 280])
        y = random.randint(-200, -50)
        speed = 5        
        super().__init__(image, x, y, speed, height)
