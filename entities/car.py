# entities/car.py

from entities.base import BaseEntity
import pygame

class Car(BaseEntity):
    def __init__(self, image, screen_width, screen_height, x_pos, y_pos):
        super().__init__(image, x_pos, y_pos)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 3

        # Combustível
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 0.05  # Quanto de combustível é consumido por frame

        # Limites de pista (você pode ajustar conforme a imagem da pista)
        self.left_limit = 100
        self.right_limit = self.screen_width - 100 - self.rect.width

    def update(self, keys):
        if self.fuel > 0:
            if keys[pygame.K_LEFT] and self.rect.x > self.left_limit:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.x < self.right_limit:
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.y < self.screen_height - self.rect.height:
                self.rect.y += self.speed

            
            # Consumir combustível
            self.fuel -= self.fuel_consumption_rate
            if self.fuel < 0:
                self.fuel = 0
                
