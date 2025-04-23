import pygame

class Car:
    def __init__(self, image, width, height):
        self.image = pygame.transform.scale(image, (60, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 30
        self.speed = 6
        self.width = width

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.width:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)