# ui/screen.py

import pygame

class Screen:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
