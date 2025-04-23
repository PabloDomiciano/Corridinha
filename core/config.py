import pygame


class Config:
    
    def __init__(self, WIDHT, HEIGHT):
        self.WIDHT = WIDHT
        self.HEIGHT = HEIGHT
    
    def inteface(self):
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Corridinha")