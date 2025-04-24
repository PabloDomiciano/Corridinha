import pygame
import random

from entities.car import Car
from entities.track import Track
from entities.fuel import FuelPickup
from entities.enemy_car import EnemyCar
from ui.hud import HUD
from ui.screen import Screen
from img.img_config import ImgConfig

class Game:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)

        # Controle de spawn de inimigos
        self.enemy_lanes = [120, 280]
        self.last_spawn_time = 0
        self.spawn_delay = 1000  # milissegundos

        # Carrega imagens
        self.img_config = ImgConfig(self.width, self.height)

        # Instancia objetos do jogo
        self.track = Track(self.img_config.track_img, self.height)
        self.car = Car(self.img_config.car_img, self.width, self.height)
        self.hud = HUD(self.screen.surface, self.car)
        self.enemies = []
        self.fuel_pickups = []

        # Imagens dos inimigos
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

        # Spawn controlado de inimigos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(600, 1500)

        # Atualiza inimigos
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.check_collision(self.car):
                print("COLISÃO! FIM DE JOGO")
                self.running = False
            elif enemy.off_screen():
                self.enemies.remove(enemy)

        # Spawn e update de combustível
        if random.random() < 0.01:
            self.fuel_pickups.append(FuelPickup(self.img_config.fuel_img, self.height))

        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if fuel.check_collision(self.car):
                print("COMBUSTÍVEL RECARREGADO!")
                self.hud.fuel = min(self.hud.max_fuel, self.hud.fuel + 20)
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen():
                self.fuel_pickups.remove(fuel)

    def spawn_enemy(self):
        # Marca faixas ocupadas
        lanes_in_use = {lane: False for lane in self.enemy_lanes}
        for enemy in self.enemies:
            for lane in self.enemy_lanes:
                if abs(enemy.rect.x - lane) < 10 and enemy.rect.y < self.height // 2:
                    lanes_in_use[lane] = True

        # Pega faixas livres
        free_lanes = [lane for lane, in_use in lanes_in_use.items() if not in_use]

        if free_lanes:
            lane = random.choice(free_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))

    def draw(self):
        self.track.draw(self.screen.surface)

        for enemy in self.enemies:
            enemy.draw(self.screen.surface)

        for fuel in self.fuel_pickups:
            fuel.draw(self.screen.surface)

        self.car.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()
