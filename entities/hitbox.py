import pygame


class Hitbox:
    def __init__(self):
        #Inicializa a colisão retangular como None
        self.rect = None

    def set_rect(self, width, height, x=0, y=0):
        #Define o tamanho do retangulo na tela
        self.rect = pygame.Rect(x, y, width, height)

    def set_from_image(self, image, x=0, y=0):
        #Passa a imagem como tamanho do hitbox
        self.rect = image.get_rect(topleft=(x, y))

    def check_rect_collision(self, other):
        #Verifica se a colisão entre 2 objetos na tela
        return self.rect.colliderect(other.rect)
    

    def draw_hitbox(self, screen, color=(255, 0, 0), thickness=2):
        if self.rect:
            #Cria o hitbox com a cor vermelha na tela
            pygame.draw.rect(screen, color, self.rect, thickness)
