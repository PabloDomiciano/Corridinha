import pygame


class Hitbox:
    def __init__(self):
        # Inicializa a colisão retangular como None
        self.rect = None

    def set_rect(self, width, height, x=0, y=0):
        """
        Define o tamanho e a posição do retângulo de colisão.
        """
        self.rect = pygame.Rect(x, y, width, height)

    def set_from_image(self, image, x=0, y=0):
        """
        Define a colisão com base nas dimensões da imagem.
        """
        self.rect = image.get_rect(topleft=(x, y))

    def check_rect_collision(self, other):
        """
        Verifica a colisão retangular entre dois objetos.
        """
        return self.rect.colliderect(other.rect)

    def draw_hitbox(self, screen, color=(255, 0, 0), thickness=2):
        """
        Método para desenhar a hitbox retangular na tela.
        Parâmetros:
            - screen: a superfície onde desenhar.
            - color: a cor do contorno da hitbox (default é vermelho).
            - thickness: espessura do contorno (default é 2).
        """
        # Desenhando a caixa retangular da hitbox
        if self.rect:
            pygame.draw.rect(screen, color, self.rect, thickness)
