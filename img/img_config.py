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

        # Caro jogador
        self.car_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "car.png")).convert_alpha(),
            (50, 90)
        )

        # Combustível
        self.fuel_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "icons", "fuel.png")).convert_alpha(),
            (50, 50)
        )

        # Ambulancia inimigo
        self.ambulancia_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "ambulancia.png")).convert_alpha(),
            (70, 110)
        )

        # Onibus inimigo
        self.onibus_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "onibus.png")).convert_alpha(),
            (70, 170)
        )

        # Carro simples inimigo
        self.car_enemy = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "cars", "car_verde.png")).convert_alpha(),
            (50, 100)
        )
        
        # Poder Fantasma
        self.ghost_power_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "icons", "fantasma.png")).convert_alpha(),
            (50, 50)
        )
        
        
        
        self.explosion_1 = pygame.transform.scale(
            pygame.image.load(os.path.join(self.asset_dir, "track", "explosion_1.png")).convert_alpha(),
            (60, 60)  # Tamanho inicial
        )

        self.explosion_2 = pygame.transform.scale(
            pygame.image.load(os.path.join(self.asset_dir, "track", "explosion_2.png")).convert_alpha(),
            (90, 90)  # Tamanho médio
        )

        self.explosion_3 = pygame.transform.scale(
            pygame.image.load(os.path.join(self.asset_dir, "track", "explosion_3.png")).convert_alpha(),
            (120, 120)  # Tamanho final
        )
        
        self.rocket_pickup_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                self.asset_dir, "weapons", "rocket.png")).convert_alpha(),
            (50, 50)
        )