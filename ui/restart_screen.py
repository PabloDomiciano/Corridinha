import pygame


class RestartScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # Fundo semi-transparente

    def mostrar_tela(self):
        # Retângulo da caixa central
        box_width, box_height = 300, 180
        box = pygame.Rect((self.screen.get_width() - box_width) // 2,
                          (self.screen.get_height() - box_height) // 2,
                          box_width, box_height)

        sim_rect = pygame.Rect(box.centerx - 110, box.bottom - 60, 80, 40)
        nao_rect = pygame.Rect(box.centerx + 30, box.bottom - 60, 80, 40)

        while True:
            self.screen.blit(self.overlay, (0, 0))
            pygame.draw.rect(self.screen, (30, 30, 30), box, border_radius=15)
            pygame.draw.rect(self.screen, (70, 70, 70),
                             sim_rect, border_radius=10)
            pygame.draw.rect(self.screen, (70, 70, 70),
                             nao_rect, border_radius=10)

            texto = self.font.render("Jogar novamente?", True, (255, 255, 255))
            texto_sim = self.font.render("Sim", True, (255, 255, 255))
            texto_nao = self.font.render("Não", True, (255, 255, 255))

            self.screen.blit(
                texto, (box.centerx - texto.get_width() // 2, box.top + 30))
            self.screen.blit(texto_sim, (sim_rect.centerx - texto_sim.get_width() // 2,
                                         sim_rect.centery - texto_sim.get_height() // 2))
            self.screen.blit(texto_nao, (nao_rect.centerx - texto_nao.get_width() // 2,
                                         nao_rect.centery - texto_nao.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sim_rect.collidepoint(event.pos):
                        return "restart"
                    elif nao_rect.collidepoint(event.pos):
                        return "quit"
