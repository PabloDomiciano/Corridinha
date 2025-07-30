# ui/hud.py
import pygame

class HUD:
    def __init__(self, surface, car, img_config):
        self.surface = surface
        self.car = car
        self.img_config = img_config
        
        # Configurações de fonte
        self.font = pygame.font.Font(None, 28)
        
        # Configurações visuais
        self.bar_width = 200
        self.bar_height = 25
        self.icon_size = 30
        self.icon_margin = 10
        self.icon_start_y = 70
        
        # Pré-carrega os ícones
        self._load_icons()

    def _load_icons(self):
        """Carrega e escala os ícones dos power-ups"""
        self.rocket_icon = pygame.transform.scale(
            self.img_config.rocket_pickup_img, 
            (self.icon_size, self.icon_size)
        )
        self.ghost_icon = pygame.transform.scale(
            self.img_config.ghost_power_img,
            (self.icon_size, self.icon_size)
        )
        self.fuel_icon = pygame.transform.scale(
            self.img_config.fuel_img,
            (self.icon_size, self.icon_size)
        )

    def update(self):
        """Atualiza os valores da HUD"""
        self.fuel_percentage = max(0, min(100, self.car.fuel))
        self.fuel_text = self.font.render(
            f"Combustível: {int(self.fuel_percentage)}%", 
            True, 
            (255, 255, 255)
        )

    def draw(self):
        """Desenha todos os elementos do HUD"""
        self._draw_background()
        self._draw_fuel_bar()
        self._draw_powerup_icons()

    def _draw_background(self):
        """Fundo semi-transparente da HUD"""
        hud_rect = pygame.Rect(10, 10, 220, 110)
        pygame.draw.rect(self.surface, (0, 0, 0, 128), hud_rect, border_radius=10)
        pygame.draw.rect(self.surface, (255, 255, 255), hud_rect, 2, border_radius=10)

    def _draw_fuel_bar(self):
        """Desenha a barra de combustível"""
        # Fundo da barra
        pygame.draw.rect(self.surface, (50, 50, 50), (20, 40, self.bar_width, self.bar_height), border_radius=8)
        
        # Barra de preenchimento
        fill_width = (self.fuel_percentage / 100) * self.bar_width
        color = (0, 200, 0) if self.fuel_percentage > 60 else \
                (200, 150, 0) if self.fuel_percentage > 30 else \
                (200, 0, 0)
        pygame.draw.rect(self.surface, color, (20, 40, fill_width, self.bar_height), border_radius=8)
        
        # Texto
        shadow = self.fuel_text.copy()
        shadow.fill((0, 0, 0))
        self.surface.blit(shadow, (21, 15))
        self.surface.blit(self.fuel_text, (20, 14))

    def _draw_powerup_icons(self):
        """Desenha os ícones dos power-ups ativos"""
        x_pos = 20
        y_pos = self.icon_start_y
        
        # Ícone de foguete
        if self.car.has_rocket:
            self.surface.blit(self.rocket_icon, (x_pos, y_pos))
            x_pos += self.icon_size + self.icon_margin
            
        # Ícone de fantasma (com efeito de piscar nos últimos segundos)
        if self.car.ghost_power_active:
            current_time = pygame.time.get_ticks()
            remaining_time = self.car.ghost_power_end_time - current_time
            
            # Mostra sempre, mas pisca nos últimos 3 segundos
            if remaining_time > self.car.blink_start_offset or current_time % 1000 < 500:
                self.surface.blit(self.ghost_icon, (x_pos, y_pos))
