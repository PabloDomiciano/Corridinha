import pygame
# Altere para importar WIDTH e HEIGHT
from config.constants import WIDTH, HEIGHT

# Defina as constantes
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT

# Defina cores padrão
COLORS = {
    "dark_blue": (0, 0, 50),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "gray": (200, 200, 200),
    "gold": (255, 215, 0)
}

class LeaderboardScreen:
    def __init__(self, score_manager):
        self.score_manager = score_manager
        # Fontes menores para tela pequena
        self.font_title = pygame.font.Font(None, 40)  # antes 64
        self.font_item = pygame.font.Font(None, 28)   # antes 36
        self.font_small = pygame.font.Font(None, 20)  # antes 24
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                return "menu"
        return None
    
    def draw(self, screen):
        screen.fill(COLORS["dark_blue"])
        
        # Título
        title = self.font_title.render("MELHORES PONTUAÇÕES", True, COLORS["yellow"])
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))  # mais no topo
        
        # Cabeçalho da tabela
        header_y = 70
        header_name = self.font_item.render("JOGADOR", True, COLORS["white"])
        header_score = self.font_item.render("PONTUAÇÃO", True, COLORS["white"])
        
        screen.blit(header_name, (SCREEN_WIDTH // 3 - header_name.get_width() // 2, header_y))
        screen.blit(header_score, (2 * SCREEN_WIDTH // 3 - header_score.get_width() // 2, header_y))
        
        # Linha separadora
        line_y = header_y + 30
        pygame.draw.line(screen, COLORS["white"], (SCREEN_WIDTH // 6, line_y), (5 * SCREEN_WIDTH // 6, line_y), 2)
        
        # Lista de pontuações
        highscores = self.score_manager.get_highscores()
        y_pos = line_y + 15
        
        for i, score_data in enumerate(highscores):
            color = COLORS["gold"] if i == 0 else COLORS["white"]
            font_size = self.font_item if i == 0 else self.font_small
            
            # Posição
            pos_text = font_size.render(f"{i+1}º", True, color)
            screen.blit(pos_text, (SCREEN_WIDTH // 6 - pos_text.get_width() // 2, y_pos))
            
            # Nome
            name_text = font_size.render(score_data["name"], True, color)
            screen.blit(name_text, (SCREEN_WIDTH // 3 - name_text.get_width() // 2, y_pos))
            
            # Pontuação
            score_text = font_size.render(str(score_data["score"]), True, color)
            screen.blit(score_text, (2 * SCREEN_WIDTH // 3 - score_text.get_width() // 2, y_pos))
            
            y_pos += 35 if i == 0 else 25  # espaçamento reduzido
        
        # Mensagem se não houver pontuações
        if not highscores:
            no_scores = self.font_item.render("Nenhuma pontuação ainda!", True, COLORS["white"])
            screen.blit(no_scores, (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, SCREEN_HEIGHT // 2))
        
        # Instrução para voltar
        instruction = self.font_small.render("Pressione ESC ou ENTER para voltar", True, COLORS["gray"])
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 30))
