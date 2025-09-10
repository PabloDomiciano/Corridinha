import pygame
# Altere para importar WIDTH e HEIGHT em vez de SCREEN_WIDTH e SCREEN_HEIGHT
from config.constants import WIDTH, HEIGHT

# Defina as constantes se não existirem no constants.py
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT

# Defina cores padrão se COLORS não existir
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "gray": (200, 200, 200)
}

class HighscoreScreen:
    def __init__(self, score_manager):
        self.score_manager = score_manager
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        self.input_text = ""
        self.active = True
        self.blink_timer = 0
        self.cursor_visible = True
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.input_text.strip():
                # SALVA A PONTUAÇÃO quando o usuário pressiona Enter
                self.score_manager.add_score(self.input_text.strip(), self.current_score)
                self.active = False  # Desativa a tela
                return "game_over"  # Vai para a tela de game over
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]  # Apaga caracteres
            elif event.key == pygame.K_ESCAPE:
                self.active = False  # Desativa a tela
                return "game_over"  # Volta sem salvar
            else:
                # ADICIONA CARACTERES ao nome
                if len(self.input_text) < 15 and event.unicode.isprintable():
                    self.input_text += event.unicode
        return None

    def update(self):
        self.blink_timer += 1
        if self.blink_timer > 30:
            self.blink_timer = 0
            self.cursor_visible = not self.cursor_visible
    
    def draw(self, screen, current_score):
        self.current_score = current_score
        screen.fill(COLORS["black"])
        
        # Primeira linha
        title1 = self.font_large.render("NOVA", True, COLORS["yellow"])
        screen.blit(title1, (SCREEN_WIDTH // 2 - title1.get_width() // 2, 60))

        # Segunda linha
        title2 = self.font_large.render("PONTUAÇÃO!", True, COLORS["yellow"])
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 120))
        
        # Pontuação
        score_text = self.font_medium.render(f"Pontuação: {current_score}", True, COLORS["white"])
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 190))
        
        # Instrução
        instruction = self.font_medium.render("Digite seu nome:", True, COLORS["white"])
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 250))
        
        # Campo de entrada
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 160, 300, 320, 45)
        pygame.draw.rect(screen, (50, 50, 50), input_rect)  # fundo cinza escuro
        pygame.draw.rect(screen, COLORS["white"], input_rect, 2)  # borda branca
        
        # Texto digitado
        if self.input_text:
            name_surface = self.font_medium.render(self.input_text, True, COLORS["white"])
            screen.blit(name_surface, (input_rect.x + 8, input_rect.y + 8))
        
        # Cursor piscante
        if self.cursor_visible and self.active:
            cursor_x = input_rect.x + 8
            if self.input_text:
                cursor_x += self.font_medium.size(self.input_text)[0]
            pygame.draw.line(screen, COLORS["white"], 
                            (cursor_x, input_rect.y + 8), 
                            (cursor_x, input_rect.y + 35), 2)
        
        # Instrução de confirmação
        confirm_text = self.font_small.render("Pressione ENTER para confirmar", True, COLORS["gray"])
        screen.blit(confirm_text, (SCREEN_WIDTH // 2 - confirm_text.get_width() // 2, 370))
        
        # Instrução de cancelamento
        cancel_text = self.font_small.render("Pressione ESC para cancelar", True, COLORS["gray"])
        screen.blit(cancel_text, (SCREEN_WIDTH // 2 - cancel_text.get_width() // 2, 410))
