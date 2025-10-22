import pygame
from config.constants import WIDTH, HEIGHT

# Dimensões da tela
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT

# Constantes de animação
ROW_DELAY_BASE = 0.1
ANIM_DURATION = 0.4
FADE_SPEED_DEFAULT = 400
START_OFFSET_FACTOR = 0.6

# Cores (mesmas da tela de ranking)
COLORS = {
    "bg_top": (6, 16, 42),
    "bg_bottom": (10, 60, 120),
    "yellow": (255, 240, 140),
    "white": (245, 245, 245),
    "muted": (180, 180, 200),
}


class CreditsScreen:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 44)
        self.font_subtitle = pygame.font.Font(None, 28)
        self.font_name = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)

        # Botão voltar
        self.back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 60, 140, 36)

        # Estado de animação (fade-in)
        self.alpha = 0
        self.fade_speed = FADE_SPEED_DEFAULT
        self.last_time = pygame.time.get_ticks()
        self.start_time = None

        # Lista de desenvolvedores
        self.developers = [
            "Pablo Henrique",
            "Eduardo Germano",
            "Renan Gondo",
            "Vinicius Ferrari"
        ]

    def _draw_gradient(self, screen):
        """Desenha o gradiente de fundo (igual ao ranking)"""
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(COLORS["bg_top"][0] * (1 - ratio) + COLORS["bg_bottom"][0] * ratio)
            g = int(COLORS["bg_top"][1] * (1 - ratio) + COLORS["bg_bottom"][1] * ratio)
            b = int(COLORS["bg_top"][2] * (1 - ratio) + COLORS["bg_bottom"][2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

    def _draw_title_and_header(self, overlay):
        """Desenha o título e cabeçalho"""
        # Título com sombra
        title_text = "CRÉDITOS"
        title = self.font_title.render(title_text, True, COLORS["yellow"])
        title_shadow = self.font_title.render(title_text, True, (10, 10, 30))
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        overlay.blit(title_shadow, (tx + 3, 24))
        overlay.blit(title, (tx, 20))

        # Subtítulo
        subtitle_y = 80
        subtitle = self.font_subtitle.render("DESENVOLVEDORES", True, COLORS["white"])
        overlay.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, subtitle_y))

        # Linha separadora
        line_y = subtitle_y + 36
        pygame.draw.line(
            overlay,
            COLORS["muted"],
            (SCREEN_WIDTH // 6, line_y),
            (5 * SCREEN_WIDTH // 6, line_y),
            2
        )
        return line_y

    def _calc_animation_offset(self, index, elapsed):
        """Calcula o offset de animação (slide-in)"""
        row_delay = ROW_DELAY_BASE * index
        p = max(0.0, (elapsed - row_delay) / ANIM_DURATION)
        p = min(1.0, p)
        # ease out cubic
        pe = 1 - (1 - p) ** 3
        start_offset = -int(SCREEN_WIDTH * START_OFFSET_FACTOR)
        offset_x = int(start_offset * (1 - pe))
        return offset_x

    def _draw_developer_row(self, overlay, index, name, y_pos, elapsed):
        """Desenha uma linha com o nome do desenvolvedor"""
        offset_x = self._calc_animation_offset(index, elapsed)

        # Nome do desenvolvedor
        name_text = self.font_name.render(name, True, COLORS["white"])
        name_x = SCREEN_WIDTH // 2 - name_text.get_width() // 2 + offset_x
        overlay.blit(name_text, (name_x, y_pos))

        # Marcador decorativo
        marker_x = name_x - 30
        pygame.draw.circle(overlay, COLORS["yellow"], (marker_x, y_pos + 12), 4)

        return y_pos + 50

    def _draw_back_button(self, overlay):
        """Desenha o botão de voltar"""
        pygame.draw.rect(overlay, (30, 30, 30), self.back_rect, border_radius=8)
        pygame.draw.rect(overlay, COLORS["muted"], self.back_rect, 2, border_radius=8)
        back_text = self.font_small.render("Voltar", True, COLORS["white"])
        overlay.blit(
            back_text,
            (
                self.back_rect.x + self.back_rect.width // 2 - back_text.get_width() // 2,
                self.back_rect.y + 6
            )
        )

    def handle_event(self, event):
        """Trata eventos de entrada (teclado e mouse)"""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                return "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # clique esquerdo
                if self.back_rect.collidepoint(event.pos):
                    return "menu"
        return None

    def update(self):
        """Atualiza a animação de fade-in"""
        now = pygame.time.get_ticks()
        dt = (now - self.last_time) / 1000.0
        self.last_time = now
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + int(self.fade_speed * dt))

    def draw(self, screen):
        """Desenha a tela de créditos"""
        # Fundo gradiente
        self._draw_gradient(screen)

        # Surface temporária para aplicar alpha do fade-in
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Título e cabeçalho
        line_y = self._draw_title_and_header(overlay)

        # Calcula tempo desde abertura (em segundos)
        now = pygame.time.get_ticks()
        elapsed = 0.0 if not self.start_time else (now - self.start_time) / 1000.0

        # Desenha lista de desenvolvedores
        y_pos = line_y + 40
        for i, dev_name in enumerate(self.developers):
            y_pos = self._draw_developer_row(overlay, i, dev_name, y_pos, elapsed)

        # Botão voltar
        self._draw_back_button(overlay)

        # Aplica alpha e copia para a tela
        overlay.set_alpha(self.alpha)
        screen.blit(overlay, (0, 0))
