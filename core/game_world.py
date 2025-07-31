import pygame
import random
from entities.player import Player
from entities.track import Track
from entities.pickups.fuel import FuelPickup
from entities.enemy_car import EnemyCar
from entities.pickups.ghost import GhostPickup

class GameWorld:
    def __init__(self, width, height, img_config):
        self.width = width
        self.height = height
        self.img_config = img_config

        # Configurações de pistas
        self.enemy_lanes = [100, 220]
<<<<<<< Updated upstream
        self.road_lanes = [100, 220]  # Adicionado para compatibilidade com ghost pickup
=======
        self.road_lanes = [100, 220]  # Compatível com ghost pickup
>>>>>>> Stashed changes

        # Controle de spawn
        self.last_spawn_time = 0
        self.spawn_delay = 1000

        # Elementos do jogo
        self.track = Track(self.img_config.track_img, self.height)
        self.car = Player(self.img_config.car_img, self.width, self.height, x_pos=200, y_pos=500)
        self.enemies = []
        self.fuel_pickups = []
<<<<<<< Updated upstream
        self.ghost_pickups = []  # Lista para gerenciar pickups de ghost
=======
        self.ghost_pickups = []
>>>>>>> Stashed changes

        # Imagens de inimigos
        self.enemy_imgs = [
            self.img_config.ambulancia_img,
            self.img_config.onibus_img,
            self.img_config.car_enemy
        ]

<<<<<<< Updated upstream
    def update(self, keys):
        self._update_track_and_player(keys)
        self._spawn_and_update_enemies()
        self._spawn_and_update_fuel()
        self._spawn_and_update_ghost_pickups()  # Novo método para ghost pickups

    def _update_track_and_player(self, keys):
        """Atualiza a pista e o jogador."""
=======
    def update(self, keys, delta_time):
        self._update_track_and_player(keys, delta_time)
        self._spawn_and_update_enemies(delta_time)
        self._spawn_and_update_fuel(delta_time)
        self._spawn_and_update_ghost_pickups(delta_time)

    def _update_track_and_player(self, keys, delta_time):
>>>>>>> Stashed changes
        self.track.update()
        self.car.update(keys, delta_time)

<<<<<<< Updated upstream
    def _spawn_and_update_enemies(self):
        """Gerencia spawn e atualização de inimigos."""
=======
    def _spawn_and_update_enemies(self, delta_time):
>>>>>>> Stashed changes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(600, 3500)

        for enemy in self.enemies[:]:
            enemy.update(delta_time)
            if enemy.off_screen(self.height):
                self.enemies.remove(enemy)

<<<<<<< Updated upstream
    def _spawn_and_update_fuel(self):
        """Gerencia spawn e atualização de combustível."""
=======
    def _spawn_and_update_fuel(self, delta_time):
>>>>>>> Stashed changes
        if random.random() < 0.005:
            lane = random.choice(self.enemy_lanes)
            self.fuel_pickups.append(FuelPickup(
                self.img_config.fuel_img, lane, self.height))

        for fuel in self.fuel_pickups[:]:
<<<<<<< Updated upstream
            fuel.update()
=======
            fuel.update(delta_time)
>>>>>>> Stashed changes
            if fuel.check_collision(self.car):
                self.car.fuel = min(self.car.max_fuel, self.car.fuel + 20)
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen(self.height):
                self.fuel_pickups.remove(fuel)

<<<<<<< Updated upstream
    def _spawn_and_update_ghost_pickups(self):
        """Gerencia spawn e atualização de ghost pickups."""
=======
    def _spawn_and_update_ghost_pickups(self, delta_time):
>>>>>>> Stashed changes
        if random.random() < 0.005:
            lane = random.choice(self.enemy_lanes)
            self.ghost_pickups.append(GhostPickup(
                self.img_config.ghost_power_img, lane, self.height))
            
        for pickup in self.ghost_pickups[:]:
            pickup.update()
            if pickup.off_screen(self.height):
                self.ghost_pickups.remove(pickup)

<<<<<<< Updated upstream


    def spawn_enemy(self):
        """Spawna um novo inimigo em pista livre."""
        lanes_in_use = {lane: False for lane in self.enemy_lanes}
        for enemy in self.enemies:
            for lane in self.enemy_lanes:
                if abs(enemy.rect.x - lane) < 5:
                    lanes_in_use[lane] = True

        free_lanes = [lane for lane, in_use in lanes_in_use.items() if not in_use]
        if free_lanes:
            lane = random.choice(free_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))

    def spawn_ghost_pickup(self):
        """Spawna um novo pickup de ghost."""
        lane = random.choice(self.road_lanes)
        self.ghost_pickups.append(GhostPickup(
            self.img_config.ghost_power_img,
            lane,
            self.height
        ))

=======
        for pickup in self.ghost_pickups[:]:
            pickup.update(delta_time)
            if pickup.off_screen(self.height):
                self.ghost_pickups.remove(pickup)

    def spawn_enemy(self):
        lanes_in_use = {lane: False for lane in self.enemy_lanes}
        for enemy in self.enemies:
            for lane in self.enemy_lanes:
                if abs(enemy.rect.x - lane) < 5:
                    lanes_in_use[lane] = True

        free_lanes = [lane for lane, in_use in lanes_in_use.items() if not in_use]
        if free_lanes:
            lane = random.choice(free_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))

    def spawn_ghost_pickup(self):
        lane = random.choice(self.road_lanes)
        self.ghost_pickups.append(GhostPickup(
            self.img_config.ghost_power_img,
            lane,
            self.height
        ))

>>>>>>> Stashed changes
    def draw(self, surface):
        """Desenha todos os elementos do jogo."""
        self.track.draw(surface)
<<<<<<< Updated upstream
        
        for enemy in self.enemies:
            enemy.draw(surface)
            
        for fuel in self.fuel_pickups:
            fuel.draw(surface)
            
        for ghost in self.ghost_pickups:
            ghost.draw(surface)
            
        self.car.draw(surface)
=======

        for enemy in self.enemies:
            enemy.draw(surface)

        for fuel in self.fuel_pickups:
            fuel.draw(surface)

        for ghost in self.ghost_pickups:
            ghost.draw(surface)

        self.car.draw(surface)
>>>>>>> Stashed changes
