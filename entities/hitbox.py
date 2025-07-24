import pygame
from config.constants import SHOW_HITBOX


class Hitbox:
    def __init__(self):
        # Inicializa a colisão retangular como None
        self.rect = None

    def set_rect(self, width, height, x=0, y=0):
        # Define o tamanho do retângulo na tela
        self.rect = pygame.Rect(x, y, width, height)

    def set_from_image(self, image, x=0, y=0):
        # Passa a imagem como tamanho do hitbox
        self.rect = image.get_rect(topleft=(x, y))

    def check_rect_collision(self, other):
        # Verifica se há colisão entre dois objetos
        return self.rect.colliderect(other.rect)

    def draw_hitbox(self, screen, color=(255, 0, 0), thickness=2):
        if SHOW_HITBOX and self.rect:
            # Desenha o hitbox apenas se a flag estiver ativada
            pygame.draw.rect(screen, color, self.rect, thickness)
