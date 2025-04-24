import pygame
from ui.screen import Screen

class ImgConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Carregamento e redimensionamento de imagens
        self.track_img = pygame.transform.scale(
            pygame.image.load("./assets/track/track.png").convert(), 
            (width, height)
        )

        self.car_img = pygame.transform.scale(
            pygame.image.load("./assets/cars/car.png").convert_alpha(),
            (80, 120)
        )


        self.fuel_img = pygame.transform.scale(
            pygame.image.load("./assets/icons/fuel.png").convert_alpha(),
            (50, 50)
        )

        self.ambulancia_img = pygame.transform.scale(
            pygame.image.load("./assets/cars/ambulancia.png").convert_alpha(),
            (100, 120)
        )

        self.onibus_img = pygame.transform.scale(
            pygame.image.load("./assets/cars/onibus.png").convert_alpha(),
            (100, 200)
        )

        self.car_enemy = pygame.transform.scale(
            pygame.image.load("./assets/cars/car.png").convert_alpha(),
            (80, 120)
        )
