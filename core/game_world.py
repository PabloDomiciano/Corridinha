import pygame
import random
from entities.pickups.rocket_pickup import RocketPickup
from entities.player import Player
from entities.track import Track
from entities.pickups.fuel import FuelPickup
from entities.enemy_car import EnemyCar
from entities.pickups.ghost import GhostPickup
from entities.explosion import Explosion  # <- Adicionado

class GameWorld:
    def __init__(self, width, height, img_config):
        self.width = width
        self.height = height
        self.img_config = img_config

        # Configurações de pistas
        self.enemy_lanes = [100, 220]
        self.road_lanes = [100, 220]

        # Controle de spawn
        self.last_spawn_time = 0
        self.spawn_delay = 1000
        self.lane_cooldowns = {lane: 0 for lane in self.enemy_lanes + self.road_lanes}
        self.last_pickup_spawn = 0
        self.pickup_cooldown = 3000  # 3 segundos entre pickups

        # Elementos do jogo
        self.track = Track(self.img_config.track_img, self.height)
        self.car = Player(self.img_config.car_img, self.width, self.height, x_pos=200, y_pos=500)
        self.enemies = []
        self.fuel_pickups = []
        self.ghost_pickups = []
        self.pickups = []

        # Explosão
        self.frozen = False  # Estado global de congelamento
        self.car.frozen = False  # Garante que o carro tem o atributo
        self.track.frozen = False  # Garante que a pista tem o atributo
        self.explosion = Explosion(img_config)  # <- Instância da explosão

        # Imagens de inimigos
        self.enemy_imgs = [
            self.img_config.ambulancia_img,
            self.img_config.onibus_img,
            self.img_config.car_enemy
        ]

    def update(self, keys):
            if self.frozen:
                self.explosion.update()  # Apenas a explosão se atualiza
                return
                
            self._update_track_and_player(keys)
            self._spawn_and_update_enemies()
            self._spawn_and_update_pickups()
            self.explosion.update()
            
            # Verifica colisões de foguetes
            if hasattr(self.car, 'rockets'):
                for rocket in self.car.rockets[:]:
                    for enemy in self.enemies[:]:
                        if rocket.rect.colliderect(enemy.rect):
                            self.create_explosion(enemy.rect.center)
                            self.enemies.remove(enemy)
                            self.car.rockets.remove(rocket)
                            break

    def create_explosion(self, position):
        self.explosion.trigger(position[0], position[1], particle_count=30)
        
    def freeze_all(self):
        """Congela todos os elementos do jogo"""
        self.frozen = True
        self.track.frozen = True
        self.car.frozen = True
            
        # Garante que todos os inimigos têm o atributo
        for enemy in self.enemies:
            if not hasattr(enemy, 'frozen'):
                enemy.frozen = False
            enemy.frozen = True
                
        # Garante que todos os pickups têm o atributo    
        for fuel in self.fuel_pickups:
            if not hasattr(fuel, 'frozen'):
                fuel.frozen = False
            fuel.frozen = True
                
        for ghost in self.ghost_pickups:
            if not hasattr(ghost, 'frozen'):
                ghost.frozen = False
            ghost.frozen = True
            
        for pickup in self.pickups:
            if not hasattr(pickup, 'frozen'):
                pickup.frozen = False
            pickup.frozen = True
            
    def unfreeze_all(self):
        """Descongela todos os elementos do jogo"""
        self.frozen = False
        self.track.frozen = False
        self.car.frozen = False
            
        for enemy in self.enemies:
            enemy.frozen = False
                
        for fuel in self.fuel_pickups:
            fuel.frozen = False
                
        for ghost in self.ghost_pickups:
            ghost.frozen = False
            
        for pickup in self.pickups:
            pickup.frozen = False
    
    def _update_track_and_player(self, keys):
        self.track.update()
        self.car.update(keys)

    # ===== SISTEMA DE SPAWN MELHORADO =====
    def _spawn_and_update_enemies(self):
        current_time = pygame.time.get_ticks()
        
        # Verifica se é hora de spawnar e se há espaço suficiente
        if (current_time - self.last_spawn_time > self.spawn_delay and 
            (len(self.enemies) == 0 or self.enemies[-1].rect.y > 150)):
            
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(1000, 2500)  # Intervalo mais controlado

        # Atualiza inimigos existentes
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.off_screen(self.height):
                self.enemies.remove(enemy)

    def spawn_enemy(self):
        now = pygame.time.get_ticks()
        available_lanes = [
            lane for lane in self.enemy_lanes 
            if now - self.lane_cooldowns[lane] > 2000  # 2s de cooldown por pista
        ]
        
        # Verifica pistas ocupadas por inimigos próximos
        for enemy in self.enemies:
            if enemy.rect.y < 250:  # Verifica inimigos na área superior
                if enemy.rect.x in available_lanes:
                    available_lanes.remove(enemy.rect.x)
        
        if available_lanes:
            lane = random.choice(available_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))
            self.lane_cooldowns[lane] = now  # Atualiza cooldown da pista
 

    def _spawn_and_update_pickups(self):
        current_time = pygame.time.get_ticks()
        
        # Spawn de fuel
        if (current_time - self.last_pickup_spawn > self.pickup_cooldown and
            random.random() < 0.005 and 
            (len(self.fuel_pickups) == 0 or self.fuel_pickups[-1].rect.y > 200)):
            
            self._spawn_fuel_pickup()
            self.last_pickup_spawn = current_time
        
        # Spawn de ghost
        if (current_time - self.last_pickup_spawn > self.pickup_cooldown and
            random.random() < 0.003 and 
            (len(self.ghost_pickups) == 0 or self.ghost_pickups[-1].rect.y > 250)):
            
            self._spawn_ghost_pickup()
            self.last_pickup_spawn = current_time
        
        # Atualiza fuel pickups (COM VERIFICAÇÃO DE COLISÃO)
        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if fuel.check_collision(self.car):  # Esta linha estava faltando
                self.car.fuel = min(self.car.max_fuel, self.car.fuel + 20)
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen(self.height):
                self.fuel_pickups.remove(fuel)
        
        # Atualiza ghost pickups
        for ghost in self.ghost_pickups[:]:
            ghost.update()
            if ghost.off_screen(self.height):
                self.ghost_pickups.remove(ghost)
                
        # Spawn da bazuca
        if (random.random() < 0.001 and  # 0.1% de chance
            len([p for p in self.pickups if isinstance(p, RocketPickup)]) == 0):
            
            lane = random.choice(self.road_lanes)
            self.pickups.append(RocketPickup(
                self.img_config.rocket_pickup_img, lane, self.height))

        # Atualiza e verifica colisão com pickups (incluindo bazuca)
        for pickup in self.pickups[:]:
            pickup.update()
            
            if pickup.off_screen(self.height):
                self.pickups.remove(pickup)
            elif pickup.check_collision(self.car):
                if isinstance(pickup, RocketPickup):
                    current_time = pygame.time.get_ticks()
                    self.car.activate_rocket_power(current_time)  # Ativa o foguete por 10 segundos
                self.pickups.remove(pickup)

    def _spawn_fuel_pickup(self):
        available_lanes = self.enemy_lanes.copy()  # Alterado para enemy_lanes
        
        # Verificação menos rigorosa
        for obj in self.enemies + self.fuel_pickups + self.ghost_pickups:
            if obj.rect.y < 150 and obj.rect.x in available_lanes:  # Reduzido para 150px
                available_lanes.remove(obj.rect.x)
        
        if available_lanes:
            lane = random.choice(available_lanes)
            self.fuel_pickups.append(FuelPickup(
                self.img_config.fuel_img, lane, self.height))

    def _spawn_ghost_pickup(self):
        available_lanes = self.road_lanes.copy()
        
        # Verificação ainda mais rigorosa para ghost pickups
        for obj in self.enemies + self.fuel_pickups + self.ghost_pickups:
            if obj.rect.y < 350 and obj.rect.x in available_lanes:
                available_lanes.remove(obj.rect.x)
        
        if available_lanes:
            lane = random.choice(available_lanes)
            self.ghost_pickups.append(GhostPickup(
                self.img_config.ghost_power_img, lane, self.height))

    # ===== FIM DO SISTEMA DE SPAWN =====

        
        
    def draw(self, surface):
        self.track.draw(surface)
        
        # Desenha todos os elementos (mesmo congelados)
        for enemy in self.enemies:
            enemy.draw(surface)
        for fuel in self.fuel_pickups:
            fuel.draw(surface)
        for ghost in self.ghost_pickups:
            ghost.draw(surface)
        for pickup in self.pickups:
            pickup.draw(surface)
        
        
                
        # Carro por último (sobre a explosão)
        self.car.draw(surface)
        # Explosão sobre os elementos
        self.explosion.draw(surface)

