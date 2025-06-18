import pygame
from entities.pickups.base_pickup import Pickup  # supondo que exista uma classe base Pickup

class SpeedBoost(Pickup):
    def __init__(self, image, x, screen_height):
        super().__init__(image, x, -image.get_height())
        self.speed = 5  # velocidade que desce a tela

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_collision(self, car):
        return self.rect.colliderect(car.rect)

    def off_screen(self, screen_height):

        return self.rect.y > screen_height
    def on_collision(self, car):
        print("SPEED BOOST ATIVADO!")
        car.speed_boost(2.0, duration=3000)  # Supondo que o carro tenha um método `speed_boost`
