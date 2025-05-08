import pygame
import random
from entities.player import Player
from entities.track import Track
from entities.fuel import FuelPickup
from entities.enemy_car import EnemyCar
from entities.explosion import Explosion
from ui.hud import HUD
from ui.screen import Screen
from img.img_config import ImgConfig


class Game:
    def __init__(self, width, height, title):
        pygame.init()

        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)

        # Controle de spawn de inimigos
        self.enemy_lanes = [100, 220]
        self.last_spawn_time = 0
        self.spawn_delay = 1000

        self.img_config = ImgConfig(self.width, self.height)

        self.track = Track(self.img_config.track_img, self.height)
        self.car = Player(self.img_config.car_img, self.width,
                          self.height, x_pos=200, y_pos=500)
        self.hud = HUD(self.screen.surface, self.car)
        self.enemies = []
        self.fuel_pickups = []
        self.explosions = []  # <- Lista de explosões

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

        pygame.quit()

    def update(self, keys):
        self.track.update()
        self.car.update(keys)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(600, 3500)

        for enemy in self.enemies[:]:
            enemy.update()

            if self.car.check_mask_collision(enemy) or self.car.check_circle_collision(enemy):
                print("COLISÃO! FIM DE JOGO")

                # Cria uma explosão na posição do carro
                explosion = Explosion(
                    self.img_config.explosion_img, self.car.rect.centerx, self.car.rect.centery)
                self.explosions.append(explosion)

                self.running = False
            elif enemy.off_screen(self.height):
                self.enemies.remove(enemy)

        if random.random() < 0.005:
            lane = random.choice(self.enemy_lanes)
            self.fuel_pickups.append(FuelPickup(
                self.img_config.fuel_img, lane, self.height))

        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if fuel.check_collision(self.car):
                print("COMBUSTÍVEL RECARREGADO!")
                self.car.fuel = min(self.car.max_fuel, self.car.fuel + 20)
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen(self.height):
                self.fuel_pickups.remove(fuel)

        # Atualiza explosões
        for explosion in self.explosions[:]:
            if explosion.is_expired():
                self.explosions.remove(explosion)

    def spawn_enemy(self):
        lanes_in_use = {lane: False for lane in self.enemy_lanes}
        for enemy in self.enemies:
            for lane in self.enemy_lanes:
                if abs(enemy.rect.x - lane) < 5:
                    lanes_in_use[lane] = True

        free_lanes = [lane for lane,
                      in_use in lanes_in_use.items() if not in_use]
        if free_lanes:
            lane = random.choice(free_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))

    def draw(self):
        self.screen.surface.fill((0, 0, 0))
        self.track.draw(self.screen.surface)

        for enemy in self.enemies:
            enemy.draw(self.screen.surface)

        for fuel in self.fuel_pickups:
            fuel.draw(self.screen.surface)

        for explosion in self.explosions:
            explosion.draw(self.screen.surface)

        self.car.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()
