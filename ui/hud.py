# ui/hud.py

import pygame

class HUD:
    def __init__(self, surface, car):
        self.surface = surface
        self.car = car
        self.font = pygame.font.Font(None, 36)  # Fonte para o texto

    def update(self):
        # Atualiza o HUD com informações do jogo
        self.fuel_text = self.font.render(f"Combustível: {int(self.car.fuel)}%", True, (255, 255, 255))
        

    def draw(self):
        # Desenha o HUD na tela
        self.surface.blit(self.fuel_text, (10, 10))  # Exibe combustível no canto superior esquerdo
