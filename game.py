import pygame
import random

from screen import Screen
from car import Car
from track import Track
from fuel import FuelPickup
from enemy_car import EnemyCar
from hud import HUD

class Game:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)

        # Carregamento e redimensionamento de imagens
        self.track_img = pygame.transform.scale(
            pygame.image.load("./assets/track/track.png").convert(), 
            (width, height)
        )
        self.car_img = pygame.image.load("./assets/cars/car.png").convert_alpha()
        self.car_img = pygame.transform.scale(self.car_img, (60, 100))
        self.fuel_img = pygame.image.load("./assets/icons/fuel.png").convert_alpha()

        self.enemy_imgs = [
            pygame.image.load("./assets/cars/ambulancia.png").convert_alpha(),
            pygame.image.load("./assets/cars/onibus.png").convert_alpha(),
            pygame.image.load("./assets/cars/car.png").convert_alpha(),
        ]

        # Instanciando objetos do jogo
        self.track = Track(self.track_img, self.height)
        self.car = Car(self.car_img, self.width, self.height)
        self.hud = HUD(self.screen.surface, self.car)
        self.enemies = []
        self.fuel_pickups = []
        self.enemy_timer = 0
        self.enemy_spawn_rate = 60

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(keys)
            self.draw()

            pygame.display.flip()

    def update(self, keys):
        self.track.update()
        self.car.update(keys)

        # Spawn de inimigos
        self.enemy_timer += 1
        if self.enemy_timer >= self.enemy_spawn_rate:
            self.enemies.append(EnemyCar(self.enemy_imgs, self.height))
            self.enemy_timer = 0
            self.enemy_spawn_rate = random.randint(40, 80)

        # Atualiza inimigos
        for enemy in self.enemies[:]:
            enemy.update()
            if self.car.rect.colliderect(enemy.rect):
                print("COLISÃO! FIM DE JOGO")
                self.running = False
            if enemy.off_screen():
                self.enemies.remove(enemy)

        # Spawn de combustível
        if random.random() < 0.01:
            self.fuel_pickups.append(FuelPickup(self.fuel_img, self.height))

        # Atualiza combustível
        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if self.car.rect.colliderect(fuel.rect):
                print("COMBUSTÍVEL RECARREGADO!")
                self.hud.fuel = min(self.hud.max_fuel, self.hud.fuel + 20)
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen():
                self.fuel_pickups.remove(fuel)

    def draw(self):
        self.track.draw(self.screen.surface)

        for enemy in self.enemies:
            enemy.draw(self.screen.surface)

        for fuel in self.fuel_pickups:
            fuel.draw(self.screen.surface)

        self.car.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()
