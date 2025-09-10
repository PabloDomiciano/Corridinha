import pygame

from config.constants import SHOW_HITBOX


class Hitbox:
    def __init__(self):
        self.rect = None

    def set_rect(self, width, height, x=0, y=0):
        self.rect = pygame.Rect(x, y, width, height)

    def set_from_image(self, image, x=0, y=0):
        self.rect = image.get_rect(topleft=(x, y))

    def check_rect_collision(self, other):
        return self.rect.colliderect(other.rect)

    def draw_hitbox(self, screen, color=(255, 0, 0), thickness=2):
        if SHOW_HITBOX and self.rect:
            pygame.draw.rect(screen, color, self.rect, thickness)