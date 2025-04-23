import pygame
import random

from screen import Screen
from car import Car
from track import Track
from fuel import FuelPickup
from enemy_car import EnemyCar
from hud import HUD
from img_config import ImgConfig

class Game:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)

        # Carrega as imagens
        self.img_config = ImgConfig(self.width, self.height)

        # Instanciando objetos do jogo com as imagens certas
        self.track = Track(self.img_config.track_img, self.height)
        self.car = Car(self.img_config.car_img, self.width, self.height)
        self.hud = HUD(self.screen.surface, self.car)
        self.enemies = []
        self.fuel_pickups = []
        self.enemy_timer = 0
        self.enemy_spawn_rate = 60

        # Lista de imagens de inimigos
        self.enemy_imgs = [
            self.img_config.ambulancia_img,
            self.img_config.onibus_img,
            self.img_config.car_enemy
        ]

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
            self.fuel_pickups.append(FuelPickup(self.img_config.fuel_img, self.height))

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
