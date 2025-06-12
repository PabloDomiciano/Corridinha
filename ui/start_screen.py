import pygame


class StartScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.title_font = pygame.font.Font(None, 64)
        self.clock = pygame.time.Clock()

    def desenhar_fundo_gradiente(self):
        for y in range(self.screen.get_height()):
            cor = 20 + int((y / self.screen.get_height()) * 60)
            pygame.draw.line(self.screen, (cor, cor, cor), (0, y), (self.screen.get_width(), y))

    def mostrar_tela(self):
        box_width, box_height = 420, 260
        box = pygame.Rect((self.screen.get_width() - box_width) // 2,
                          (self.screen.get_height() - box_height) // 2,
                          box_width, box_height)

        iniciar_rect = pygame.Rect(box.centerx - 120, box.bottom - 80, 100, 45)
        sair_rect = pygame.Rect(box.centerx + 20, box.bottom - 80, 100, 45)

        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            self.desenhar_fundo_gradiente()

            # Sombra da caixa
            sombra = box.copy()
            sombra.x += 4
            sombra.y += 4
            pygame.draw.rect(self.screen, (0, 0, 0, 80), sombra, border_radius=20)

            # Caixa principal
            pygame.draw.rect(self.screen, (40, 40, 40), box, border_radius=20)
            pygame.draw.rect(self.screen, (100, 100, 100), box, 2, border_radius=20)

            # Botões
            self.desenhar_botao(iniciar_rect, "Iniciar", mouse_pos)
            self.desenhar_botao(sair_rect, "Sair", mouse_pos)

            # Título
            titulo = self.title_font.render("Corrida 2D", True, (255, 255, 255))
            self.screen.blit(titulo, (box.centerx - titulo.get_width() // 2, box.top + 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "sair"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if iniciar_rect.collidepoint(event.pos):
                        return "iniciar"
                    elif sair_rect.collidepoint(event.pos):
                        return "sair"

    def desenhar_botao(self, rect, texto, mouse_pos):
        cor_base = (90, 90, 90)
        cor_hover = (120, 120, 120)
        cor = cor_hover if rect.collidepoint(mouse_pos) else cor_base

        pygame.draw.rect(self.screen, cor, rect, border_radius=10)
        pygame.draw.rect(self.screen, (150, 150, 150), rect, 2, border_radius=10)

        texto_render = self.font.render(texto, True, (255, 255, 255))
        self.screen.blit(texto_render, (
            rect.centerx - texto_render.get_width() // 2,
            rect.centery - texto_render.get_height() // 2
        ))
