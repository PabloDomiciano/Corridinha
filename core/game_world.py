import pygame
import random
from entities.player import Player
from entities.track import Track
from entities.fuel import FuelPickup
from entities.enemy_car import EnemyCar


class GameWorld:
    def __init__(self, width, height, img_config):
        self.width = width
        self.height = height
        self.img_config = img_config

        # Controle de spawn de inimigos
        self.enemy_lanes = [100, 220]
        self.last_spawn_time = 0
        self.spawn_delay = 1000

        self.track = Track(self.img_config.track_img, self.height)
        self.car = Player(self.img_config.car_img, self.width,
                          self.height, x_pos=200, y_pos=500)
        self.enemies = []
        self.fuel_pickups = []

        self.enemy_imgs = [
            self.img_config.ambulancia_img,
            self.img_config.onibus_img,
            self.img_config.car_enemy
        ]

    def update(self, keys):
        # Atualiza o estado da pista e do carro
        self.track.update()
        self.car.update(keys)

        # Verificação de tempo para o spawn de inimigos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(600, 3500)

        # Atualiza os inimigos
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.off_screen(self.height):
                self.enemies.remove(enemy)

        # Spawn de combustível
        if random.random() < 0.005:
            lane = random.choice(self.enemy_lanes)
            self.fuel_pickups.append(FuelPickup(
                self.img_config.fuel_img, lane, self.height))

        # Atualiza e verifica colisões de combustível
        for fuel in self.fuel_pickups[:]:
            fuel.update()
            # Verifica a colisão do combustível com o carro
            if fuel.check_collision(self.car):
                print("COMBUSTÍVEL RECARREGADO!")
                self.car.fuel = min(self.car.max_fuel, self.car.fuel + 20)
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen(self.height):
                self.fuel_pickups.remove(fuel)

        # Verifica colisões com os inimigos
        for enemy in self.enemies[:]:
            # Verifica colisão entre o carro e os inimigos
            if self.car.check_hitbox_collision(enemy):
                print("COLISÃO COM INIMIGO! FIM DE JOGO!")
                self.running = False

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

    def draw(self, surface):
        # Desenha a pista, os inimigos, o combustível e o carro
        self.track.draw(surface)

        for enemy in self.enemies:
            enemy.draw(surface)  # Desenha os inimigos e suas hitboxes

        for fuel in self.fuel_pickups:
            fuel.draw(surface)  # Desenha o combustível e sua hitbox

        self.car.draw(surface)  # Desenha o carro e sua hitbox
