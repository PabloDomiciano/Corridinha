# img/img_config.py

import pygame
import os


class ImgConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Diretório base para as imagens
        self.asset_dir = "./assets"

        # Carregamento e redimensionamento de imagens

        # Pista
        self.track_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "track", "track.png")).convert(),
            (width, height)
        )

        # Carro do jogador
        self.car_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "car.png")).convert_alpha(),
            (50, 90)
        )

        # Imagem de combustível
        self.fuel_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "icons", "fuel.png")).convert_alpha(),
            (50, 50)
        )

        # Imagens dos carros inimigos
        self.ambulancia_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "ambulancia.png")).convert_alpha(),
            (70, 110)
        )

        self.onibus_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "onibus.png")).convert_alpha(),
            (70, 170)
        )

        self.car_enemy = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "car.png")).convert_alpha(),
            (60, 100)
        )

        # Explosão
        #self.track_img = pygame.transform.scale(
            #pygame.image.load(os.path.join(
                #self.asset_dir, "cars", "explosao.png")).convert(),
            #(80, 120)
        #)
