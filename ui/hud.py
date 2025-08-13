# ui/hud.py
import pygame

class HUD:
    def __init__(self, surface, car, img_config, score_ref):
        self.surface = surface
        self.car = car
        self.img_config = img_config
        self.score_ref = score_ref  # função que retorna o score atual
        
        # Fonte menor para caber no bloco
        self.font = pygame.font.Font(None, 30)
        
        # Configurações visuais
        self.bar_width = 120
        self.bar_height = 18
        self.icon_size = 25
        self.icon_margin = 5
        self.icon_start_y = 65

        # Posição do bloco fora da pista (lado esquerdo)
        self.hud_x = 10
        self.hud_y = 10
        self.hud_width = 180
        self.hud_height = 100
        
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
            f"{ int(self.fuel_percentage)}%", True, (255, 255, 255)
        )
        self.score_text = self.font.render(
            f"Score: {int(self.score_ref())}", True, (255, 255, 255)
        )

    def draw(self):
        """Desenha todos os elementos do HUD"""
        self._draw_background()
        self._draw_score()
        self._draw_fuel_bar()
        self._draw_powerup_icons()

    def _draw_background(self):
        """Fundo semi-transparente da HUD"""
        hud_rect = pygame.Rect(self.hud_x, self.hud_y, self.hud_width, self.hud_height)
        pygame.draw.rect(self.surface, (0, 0, 0, 128), hud_rect, border_radius=10)
        pygame.draw.rect(self.surface, (255, 255, 255), hud_rect, 2, border_radius=10)

    def _draw_score(self):
        """Desenha o texto de pontuação na parte superior"""
        self.surface.blit(self.score_text, (self.hud_x + 10, self.hud_y + 5))

    def _draw_fuel_bar(self):
        """Desenha a barra de combustível"""
        bar_x = self.hud_x + 10
        bar_y = self.hud_y + 25
        
        # Ícone de combustível
        self.surface.blit(self.fuel_icon, (bar_x, bar_y - 2))
        
        # Fundo da barra
        pygame.draw.rect(self.surface, (50, 50, 50),
                         (bar_x + self.icon_size + 5, bar_y,
                          self.bar_width, self.bar_height), border_radius=6)
        
        # Barra de preenchimento
        fill_width = (self.fuel_percentage / 100) * self.bar_width
        color = (0, 200, 0) if self.fuel_percentage > 60 else \
                (200, 150, 0) if self.fuel_percentage > 30 else \
                (200, 0, 0)
        pygame.draw.rect(self.surface, color,
                         (bar_x + self.icon_size + 5, bar_y,
                          fill_width, self.bar_height), border_radius=6)
        
        # Texto da porcentagem
        self.surface.blit(self.fuel_text, (bar_x + self.icon_size + self.bar_width - 15, bar_y - 2))

    def _draw_powerup_icons(self):
        """Desenha os ícones dos power-ups ativos"""
        x_pos = self.hud_x + 10
        y_pos = self.hud_y + self.icon_start_y
        
        # Ícone de foguete
        if self.car.has_rocket:
            self.surface.blit(self.rocket_icon, (x_pos, y_pos))
            x_pos += self.icon_size + self.icon_margin
            
        # Ícone de fantasma
        if self.car.ghost_power_active:
            current_time = pygame.time.get_ticks()
            remaining_time = self.car.ghost_power_end_time - current_time
            if remaining_time > self.car.blink_start_offset or current_time % 1000 < 500:
                self.surface.blit(self.ghost_icon, (x_pos, y_pos))
