import pygame


class BaseEntity:
    def __init__(self, image, x_pos, y_pos):
        if image is None:
            # Cria uma superfície vermelha como fallback
            self.image = pygame.Surface((50, 30))
            self.image.fill((255, 0, 0))
            print("Aviso: Imagem None substituída por fallback")
        else:
            self.image = image
            
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.frozen = False

    def draw(self, surface):
        try:
            surface.blit(self.image, self.rect)
        except:
            print("Erro ao desenhar entidade")