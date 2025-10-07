import pygame
from config.constants import WIDTH, HEIGHT

# Dimensões da tela (importadas do projeto)
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT

# ---- Constantes de aparência e animação ----
ROW_DELAY_BASE = 0.08
ANIM_DURATION = 0.35
FADE_SPEED_DEFAULT = 400  # alpha por segundo
START_OFFSET_FACTOR = 0.6  # porcentagem da largura usada para o offset inicial da animação

# Cores (centralizadas)
COLORS = {
    "bg_top": (6, 16, 42),
    "bg_bottom": (10, 60, 120),
    "yellow": (255, 240, 140),
    "white": (245, 245, 245),
    "muted": (180, 180, 200),
    "gold": (255, 200, 0),
    "silver": (200, 200, 220),
    "bronze": (205, 127, 50),
}

# Mapeamento de cores por posição (top3)
TOP_COLORS = {
    0: COLORS["gold"],
    1: COLORS["silver"],
    2: COLORS["bronze"],
}


class LeaderboardScreen:
    def __init__(self, score_manager):
        self.score_manager = score_manager
        self.font_title = pygame.font.Font(None, 44)
        self.font_item = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 20)

        # Botão voltar (rect)
        self.back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 60, 140, 36)

        # Estado de animação (fade-in)
        self.alpha = 0
        self.fade_speed = FADE_SPEED_DEFAULT  # unidades de alpha por segundo (aprox)
        self.last_time = pygame.time.get_ticks()
        # Tempo de início para animações (slide-in)
        self.start_time = None

    # ---- Helpers de desenho e animação ----
    def _draw_gradient(self, screen):
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(COLORS["bg_top"][0] * (1 - ratio) + COLORS["bg_bottom"][0] * ratio)
            g = int(COLORS["bg_top"][1] * (1 - ratio) + COLORS["bg_bottom"][1] * ratio)
            b = int(COLORS["bg_top"][2] * (1 - ratio) + COLORS["bg_bottom"][2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

    def _draw_title_and_header(self, overlay):
        # Título com sombra
        title_text = "MELHORES PONTUA\u00c7\u00d5ES"
        title = self.font_title.render(title_text, True, COLORS["yellow"])
        title_shadow = self.font_title.render(title_text, True, (10, 10, 30))
        tx = SCREEN_WIDTH // 2 - title.get_width() // 2
        overlay.blit(title_shadow, (tx + 3, 24))
        overlay.blit(title, (tx, 20))

        # Cabeçalho
        header_y = 80
        header_name = self.font_item.render("JOGADOR", True, COLORS["white"])
        header_score = self.font_item.render("PONTUA\u00c7\u00c3O", True, COLORS["white"])
        overlay.blit(header_name, (SCREEN_WIDTH // 3 - header_name.get_width() // 2, header_y))
        overlay.blit(header_score, (2 * SCREEN_WIDTH // 3 - header_score.get_width() // 2, header_y))

        # Linha separadora
        line_y = header_y + 36
        pygame.draw.line(overlay, COLORS["muted"], (SCREEN_WIDTH // 6, line_y), (5 * SCREEN_WIDTH // 6, line_y), 2)
        return line_y

    def _calc_animation_offset(self, index, elapsed):
        row_delay = ROW_DELAY_BASE * index
        p = max(0.0, (elapsed - row_delay) / ANIM_DURATION)
        p = min(1.0, p)
        # ease out cubic
        pe = 1 - (1 - p) ** 3
        start_offset = -int(SCREEN_WIDTH * START_OFFSET_FACTOR)
        offset_x = int(start_offset * (1 - pe))
        return offset_x

    def _draw_row(self, overlay, i, score_data, y_pos, elapsed):
        is_top = i < 3
        accent = TOP_COLORS.get(i, COLORS["white"]) if is_top else COLORS["white"]
        font_use = self.font_item if i == 0 else self.font_small

        offset_x = self._calc_animation_offset(i, elapsed)

        # Texto pos/nome/score com cor de destaque para top3
        text_color = accent if is_top else COLORS["white"]
        pos_text = font_use.render(f"{i+1}\u00ba", True, text_color)
        overlay.blit(pos_text, (SCREEN_WIDTH // 6 - pos_text.get_width() // 2 + 10 + offset_x, y_pos))

        name = score_data.get("name", "-")
        name_text = font_use.render(name, True, text_color)
        overlay.blit(name_text, (SCREEN_WIDTH // 3 - name_text.get_width() // 2 + offset_x, y_pos))

        score_text = font_use.render(str(score_data.get("score", 0)), True, text_color)
        overlay.blit(score_text, (2 * SCREEN_WIDTH // 3 - score_text.get_width() // 2 + offset_x, y_pos))

        return y_pos + (46 if i == 0 else 32)

    def _draw_back_button(self, overlay):
        pygame.draw.rect(overlay, (30, 30, 30), self.back_rect, border_radius=8)
        pygame.draw.rect(overlay, COLORS["muted"], self.back_rect, 2, border_radius=8)
        back_text = self.font_small.render("Voltar", True, COLORS["white"])
        overlay.blit(back_text, (self.back_rect.x + self.back_rect.width // 2 - back_text.get_width() // 2, self.back_rect.y + 6))

    def handle_event(self, event):
        # Fecha a tela com ESC ou ENTER
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                return "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # clique esquerdo
                if self.back_rect.collidepoint(event.pos):
                    return "menu"
        return None

    def update(self):
        # Atualiza o fade-in
        now = pygame.time.get_ticks()
        dt = (now - self.last_time) / 1000.0
        self.last_time = now
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + int(self.fade_speed * dt))
        # Se start_time definido, nada extra aqui; draw usa o start_time para calcular o slide

    def draw(self, screen):
        # Fundo gradiente
        self._draw_gradient(screen)

        # Surface temporária para aplicar alpha do fade-in
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Título / cabeçalho
        line_y = self._draw_title_and_header(overlay)

        # Desenha a lista
        highscores = self.score_manager.get_highscores()
        y_pos = line_y + 20

        # calcula tempo desde abertura (em segundos)
        now = pygame.time.get_ticks()
        elapsed = 0.0 if not self.start_time else (now - self.start_time) / 1000.0

        for i, score_data in enumerate(highscores):
            y_pos = self._draw_row(overlay, i, score_data, y_pos, elapsed)

        # Se não tiver pontuações
        if not highscores:
            no_scores = self.font_item.render("Nenhuma pontuação ainda!", True, COLORS["white"]) 
            overlay.blit(no_scores, (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, SCREEN_HEIGHT // 2))

        # Botão voltar (visual)
        self._draw_back_button(overlay)

        # Aplica alpha e copia para a tela
        overlay.set_alpha(self.alpha)
        screen.blit(overlay, (0, 0))
