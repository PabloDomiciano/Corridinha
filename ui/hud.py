# ui/hud.py

import pygame

class HUD:
    def __init__(self, surface, car):
        self.surface = surface
        self.car = car
        self.font = pygame.font.Font(None, 28) # Tamanho da fonte
        self.bar_width = 200
        self.bar_height = 25

    def update(self):
        self.fuel_percentage = max(0, min(100, self.car.fuel))  # Garante entre 0 e 100
        self.fuel_text = self.font.render(f"Combustível: {int(self.fuel_percentage)}%", True, (255, 255, 255))

    def draw(self):
        # HUD background com transparência e bordas arredondadas
        hud_rect = pygame.Rect(10, 10, 220, 60)
        pygame.draw.rect(self.surface, (0, 0, 0, 128), hud_rect, border_radius=10)

        # Desenha contorno da caixa
        pygame.draw.rect(self.surface, (255, 255, 255), hud_rect, 2, border_radius=10)

        # Barra de combustível - fundo
        bar_bg_rect = pygame.Rect(20, 40, self.bar_width, self.bar_height)
        pygame.draw.rect(self.surface, (50, 50, 50), bar_bg_rect, border_radius=8)

        # Barra de combustível - preenchimento
        fill_width = (self.fuel_percentage / 100) * self.bar_width
        bar_fill_rect = pygame.Rect(20, 40, fill_width, self.bar_height)

        # Cor muda conforme combustível
        if self.fuel_percentage > 60:
            color = (0, 200, 0)  # Verde
        elif self.fuel_percentage > 30:
            color = (200, 150, 0)  # Amarelo
        else:
            color = (200, 0, 0)  # Vermelho

        pygame.draw.rect(self.surface, color, bar_fill_rect, border_radius=8)

        # Texto com sombra
        shadow = self.fuel_text.copy()
        shadow.fill((0, 0, 0))
        self.surface.blit(shadow, (21, 15))  # Sombra deslocada
        self.surface.blit(self.fuel_text, (20, 14))  # Texto principal
