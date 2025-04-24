import random
from entities.base_car import BaseCar
from img.img_config import ImgConfig

class EnemyCar(BaseCar):
    def __init__(self, image, x, height):
        y = random.randint(-200, -100)
        speed = random.randint(4, 7)
        super().__init__(image, x, y, speed, height)
