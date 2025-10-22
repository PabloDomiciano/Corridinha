import pygame


class FloatingText:
    """Texto flutuante que sobe e desaparece (ex: pontos ganhos)"""

    def __init__(self, text, x, y, color=(255, 215, 0), font_size=24, duration=1500):
        """
        text: texto a ser exibido (ex: "+20")
        x, y: posição inicial
        color: cor do texto (padrão: dourado)
        font_size: tamanho da fonte
        duration: duração em ms até desaparecer
        """
        self.text = text
        self.x = x
        self.y = y
        self.start_y = y
        self.color = color
        self.font_size = font_size
        self.duration = duration
        self.birth_time = pygame.time.get_ticks()
        self.alpha = 255  # Opacidade inicial
        self.rise_speed = 0.5  # Velocidade de subida
        
        # Cria a fonte e renderiza o texto
        self.font = pygame.font.Font(None, font_size)
        self.surface = self.font.render(text, True, color)
        self.rect = self.surface.get_rect(center=(x, y))

    def update(self, dt=1/60):
        """Atualiza a posição e opacidade do texto"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.birth_time
        
        # Move o texto para cima (velocidade multiplicada por 60 para manter mesma velocidade em 60 FPS)
        self.y -= self.rise_speed * 60 * dt
        self.rect.centery = int(self.y)
        
        # Calcula a opacidade (fade out)
        progress = elapsed / self.duration
        self.alpha = int(255 * (1 - progress))
        
        # Atualiza a superfície com a nova opacidade
        self.surface = self.font.render(self.text, True, self.color)
        self.surface.set_alpha(self.alpha)
        
    def is_expired(self):
        """Verifica se o texto já expirou"""
        current_time = pygame.time.get_ticks()
        return (current_time - self.birth_time) >= self.duration
    
    def draw(self, surface):
        """Desenha o texto na tela"""
        surface.blit(self.surface, self.rect)
