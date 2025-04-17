import pygame
import os

class HUD:
    def __init__(self, screen, car):
        self.screen = screen
        self.car = car
        self.fuel = 100
        self.max_fuel = 100

        self.font = pygame.font.SysFont("Arial", 24)

        # Cores
        self.bg_color = (0, 0, 0, 180)      # Fundo escuro semi-transparente
        self.text_color = (255, 255, 255)
        self.fuel_color = (50, 205, 50)     # Verde combustível
        self.fuel_bg_color = (100, 100, 100)

        # Área do HUD (canto superior esquerdo)
        self.hud_rect = pygame.Rect(10, 10, 220, 80)

    def update(self):
        self.fuel -= 0.05
        if self.fuel < 0:
            self.fuel = 0

    def draw(self):
        # Fundo do HUD
        pygame.draw.rect(self.screen, self.bg_color, self.hud_rect, border_radius=10)

        # Texto de combustível
        fuel_text = self.font.render(f"Fuel: {int(self.fuel)}%", True, self.text_color)
        self.screen.blit(fuel_text, (self.hud_rect.x + 10, self.hud_rect.y + 10))

        # Barra de combustível
        fuel_bar_width = int((self.fuel / self.max_fuel) * 180)
        pygame.draw.rect(self.screen, self.fuel_bg_color,
            (self.hud_rect.x + 10, self.hud_rect.y + 40, 180, 10), border_radius=5)
        pygame.draw.rect(self.screen, self.fuel_color,
            (self.hud_rect.x + 10, self.hud_rect.y + 40, fuel_bar_width, 10), border_radius=5)

        # Velocidade abaixo da barra
        speed_text = self.font.render(f"Speed: {int(self.car.speed) * 10} km/h", True, self.text_color)
        self.screen.blit(speed_text, (self.hud_rect.x + 10, self.hud_rect.y + 58))
