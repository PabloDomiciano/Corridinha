<<<<<<< Updated upstream
# ui/hud.py

=======
>>>>>>> Stashed changes
import pygame

class HUD:
    def __init__(self, surface, car):
        self.surface = surface
        self.car = car
<<<<<<< Updated upstream
        self.font = pygame.font.Font(None, 28) # Tamanho da fonte
        self.bar_width = 200
        self.bar_height = 25

    def update(self):
        self.fuel_percentage = max(0, min(100, self.car.fuel))  # Garante entre 0 e 100
        self.fuel_text = self.font.render(f"Combustível: {int(self.fuel_percentage)}%", True, (255, 255, 255))

    def draw(self):
        # HUD background com transparência e bordas arredondadas
        hud_rect = pygame.Rect(10, 10, 220, 60)
=======
        self.img_config = img_config
        
        # Fonte e estilo
        self.font = pygame.font.Font(None, 28)
        self.bar_width = 200
        self.bar_height = 25
        self.icon_size = 30
        self.icon_margin = 10
        self.icon_start_y = 70
        
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
        """Atualiza os dados exibidos"""
        self.fuel_percentage = max(0, min(100, self.car.fuel))
        self.fuel_text = self.font.render(
            f"Combustível: {int(self.fuel_percentage)}%", 
            True, 
            (255, 255, 255)
        )

    def draw(self):
        """Desenha toda a HUD"""
        self._draw_background()
        self._draw_fuel_bar()
        self._draw_powerup_icons()

    def _draw_background(self):
        """Fundo da HUD"""
        hud_rect = pygame.Rect(10, 10, 220, 110)
>>>>>>> Stashed changes
        pygame.draw.rect(self.surface, (0, 0, 0, 128), hud_rect, border_radius=10)

        # Desenha contorno da caixa
        pygame.draw.rect(self.surface, (255, 255, 255), hud_rect, 2, border_radius=10)

<<<<<<< Updated upstream
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
=======
    def _draw_fuel_bar(self):
        """Desenha barra de combustível"""
        pygame.draw.rect(self.surface, (50, 50, 50), (20, 40, self.bar_width, self.bar_height), border_radius=8)
        
        fill_width = (self.fuel_percentage / 100) * self.bar_width
        color = (
            (0, 200, 0) if self.fuel_percentage > 60 else
            (200, 150, 0) if self.fuel_percentage > 30 else
            (200, 0, 0)
        )
        pygame.draw.rect(self.surface, color, (20, 40, fill_width, self.bar_height), border_radius=8)
>>>>>>> Stashed changes

        # Texto com sombra
        shadow = self.fuel_text.copy()
        shadow.fill((0, 0, 0))
<<<<<<< Updated upstream
        self.surface.blit(shadow, (21, 15))  # Sombra deslocada
        self.surface.blit(self.fuel_text, (20, 14))  # Texto principal
=======
        self.surface.blit(shadow, (21, 15))
        self.surface.blit(self.fuel_text, (20, 14))

    def _draw_powerup_icons(self):
        """Exibe ícones dos power-ups ativos"""
        x_pos = 20
        y_pos = self.icon_start_y

        # Rocket ativo
        if hasattr(self.car, "has_rocket") and self.car.has_rocket:
            self.surface.blit(self.rocket_icon, (x_pos, y_pos))
            x_pos += self.icon_size + self.icon_margin

        # Ghost ativo
        if hasattr(self.car, "ghost_power_active") and self.car.ghost_power_active:
            current_time = pygame.time.get_ticks()
            remaining = self.car.ghost_power_end_time - current_time
            if remaining > self.car.blink_start_offset or (current_time % 1000 < 500):
                self.surface.blit(self.ghost_icon, (x_pos, y_pos))
>>>>>>> Stashed changes
