import pygame


class Image:

    def __init__(self, car_img, car_enemy):
        self.car_img = car_img
        self.car_enemy = car_enemy

    def definindo_imagem_carro(self, car_img):
        self.car_img = pygame.image.load(
            '../assets/cars/car.png').convert_alpha()
        self.car_img = pygame.transform.scale(car_img, (120, 200))

    def definindo_imagem_carro_inimigo(self, car_enemy):
        self.car_enemy = pygame.image.load(
            '../assets/cars/car.png').convert_alpha()
        self.car_enemy = pygame.transform.scale(car_enemy, (120, 200))
