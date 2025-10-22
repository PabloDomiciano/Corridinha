import pygame
import random
from entities.pickups.rocket_pickup import RocketPickup
from entities.player import Player
from entities.track import Track
from entities.pickups.fuel import FuelPickup
from entities.enemy_car import EnemyCar
from entities.pickups.ghost import GhostPickup
from entities.explosion import Explosion  # <- Adicionado
from entities.floating_text import FloatingText  # <- Adicionado para pontos flutuantes


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
        self.pickup_cooldown = 2000  # Reduzido de 3000 para 2000ms (mais frequente)
        self.last_fuel_spawn = 0
        self.fuel_spawn_cooldown = 4000  # Cooldown específico para fuel (4 segundos)

        # Elementos do jogo
        self.track = Track(self.img_config.track_img, self.height)
        self.car = Player(
            self.img_config.car_img, self.width, self.height, x_pos=200, y_pos=500
        )
        self.enemies = []
        self.fuel_pickups = []
        self.ghost_pickups = []
        self.pickups = []

        # Explosão
        self.frozen = False  # Estado global de congelamento
        self.car.frozen = False  # Garante que o carro tem o atributo
        self.track.frozen = False  # Garante que a pista tem o atributo
        self.explosion = Explosion(img_config)  # <- Instância da explosão
        
        # Textos flutuantes (para pontos)
        self.floating_texts = []
        
        # Distância percorrida (para pontuação)
        self.distance_traveled = 0

        # Imagens de inimigos
        self.enemy_imgs = [
            self.img_config.ambulancia_img,
            self.img_config.onibus_img,
            self.img_config.car_enemy,
        ]

    def update(self, keys):
        if self.frozen:
            self.explosion.update()  
            return

        current_time = pygame.time.get_ticks() 
        
        self._update_track_and_player(keys)
        self._spawn_and_update_enemies()
        self._spawn_and_update_pickups()
        self.explosion.update()
        self.car.update_ghost_power(current_time)
        
        # Atualiza distância percorrida (baseado na velocidade da pista)
        self.distance_traveled += self.track.speed

        # Atualiza e remove textos flutuantes expirados
        for text in self.floating_texts[:]:
            text.update()
            if text.is_expired():
                self.floating_texts.remove(text)

        if hasattr(self.car, "rockets"):
            for rocket in self.car.rockets[:]:
                for enemy in self.enemies[:]:
                    if rocket.rect.colliderect(enemy.rect):
                        self.create_explosion(enemy.rect.center)
                        
                        # Cria texto flutuante de pontos
                        self.create_floating_text(
                            "+20", 
                            enemy.rect.centerx, 
                            enemy.rect.top - 10
                        )
                        
                        # Adiciona pontos ao bonus_score (não ao score diretamente)
                        if hasattr(self, "game_manager"):
                            self.game_manager.bonus_score += 20
                        
                        self.enemies.remove(enemy)
                        self.car.rockets.remove(rocket)
                        break
                # Remove foguetes que saíram da tela
                if rocket.rect.bottom < 0:
                    self.car.rockets.remove(rocket)

    def create_explosion(self, position):
        self.explosion.trigger(position[0], position[1], particle_count=30)

        # Toca o som da explosão
        if hasattr(self, "game_manager") and hasattr(
            self.game_manager, "explosion_sound"
        ):
            self.game_manager.explosion_sound.play()
    
    def create_floating_text(self, text, x, y):
        """Cria um texto flutuante (ex: pontos ganhos)"""
        floating_text = FloatingText(
            text=text,
            x=x,
            y=y,
            color=(255, 215, 0),  # Dourado
            font_size=28,
            duration=1500
        )
        self.floating_texts.append(floating_text)

    def freeze_all(self):
        """Congela todos os elementos do jogo"""
        self.frozen = True
        self.track.frozen = True
        self.car.frozen = True

        # Garante que todos os inimigos têm o atributo
        for enemy in self.enemies:
            if not hasattr(enemy, "frozen"):
                enemy.frozen = False
            enemy.frozen = True

        # Garante que todos os pickups têm o atributo
        for fuel in self.fuel_pickups:
            if not hasattr(fuel, "frozen"):
                fuel.frozen = False
            fuel.frozen = True

        for ghost in self.ghost_pickups:
            if not hasattr(ghost, "frozen"):
                ghost.frozen = False
            ghost.frozen = True

        for pickup in self.pickups:
            if not hasattr(pickup, "frozen"):
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
        if current_time - self.last_spawn_time > self.spawn_delay and (
            len(self.enemies) == 0 or self.enemies[-1].rect.y > 150
        ):
            # NOVA VERIFICAÇÃO: Verifica se não está criando um bloqueio total
            if not self._would_create_blockage():
                self.spawn_enemy()
                self.last_spawn_time = current_time
                self.spawn_delay = random.randint(1000, 2500)  # Intervalo mais controlado

        # Atualiza inimigos existentes (passando a posição do player e outros inimigos)
        for enemy in self.enemies[:]:
            enemy.update(self.car.rect, self.enemies)  # Passa a posição do player e lista de inimigos
            if enemy.off_screen(self.height):
                self.enemies.remove(enemy)
    
    def _would_create_blockage(self):
        """Verifica se spawnar um novo inimigo criaria um bloqueio total para o player"""
        # Verifica se há inimigos muito próximos um do outro formando uma "parede"
        # que bloquearia completamente a passagem do player
        
        # Agrupa inimigos por faixas de Y (altura similar = possível bloqueio)
        y_ranges = []
        blockage_threshold = 100  # Distância Y que considera como "mesma linha"
        
        for enemy in self.enemies:
            # Só considera inimigos que estão visíveis e à frente do player
            if 0 < enemy.rect.y < self.height and enemy.rect.y < self.car.rect.y + 200:
                # Verifica se já existe um range Y similar
                found_range = False
                for y_range in y_ranges:
                    if abs(y_range['y'] - enemy.rect.y) < blockage_threshold:
                        y_range['lanes'].add(enemy.rect.x)
                        found_range = True
                        break
                
                if not found_range:
                    y_ranges.append({'y': enemy.rect.y, 'lanes': {enemy.rect.x}})
        
        # Verifica se alguma "linha" de inimigos ocupa todas as faixas
        for y_range in y_ranges:
            if len(y_range['lanes']) >= len(self.enemy_lanes):
                # Todas as faixas ocupadas nessa altura = bloqueio total
                return True
        
        return False

    def spawn_enemy(self):
        now = pygame.time.get_ticks()
        available_lanes = [
            lane
            for lane in self.enemy_lanes
            if now - self.lane_cooldowns[lane] > 2000  # 2s de cooldown por pista
        ]

        # Verifica pistas ocupadas por inimigos próximos
        occupied_lanes = []
        for enemy in self.enemies:
            if enemy.rect.y < 250:  # Verifica inimigos na área superior
                if enemy.rect.x in available_lanes and enemy.rect.x not in occupied_lanes:
                    occupied_lanes.append(enemy.rect.x)

        # Remove pistas ocupadas das disponíveis
        for lane in occupied_lanes:
            if lane in available_lanes:
                available_lanes.remove(lane)
        
        # NOVA VERIFICAÇÃO: Garante que sempre haverá pelo menos UMA faixa livre
        # Se todas as faixas foram ocupadas recentemente, não spawna nada
        # Isso garante que o player sempre terá espaço para passar
        if len(occupied_lanes) >= len(self.enemy_lanes):
            # Todas as faixas estão ocupadas, não spawna para deixar espaço
            return
        
        if available_lanes:
            lane = random.choice(available_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))
            self.lane_cooldowns[lane] = now  # Atualiza cooldown da pista

    def _spawn_and_update_pickups(self):
        current_time = pygame.time.get_ticks()

        # Spawn de fuel - SISTEMA MELHORADO E CONTROLADO
        # Spawn automático se:
        # 1. Passou o cooldown
        # 2. Não há fuel na tela OU o último está longe o suficiente
        # 3. O combustível do player está abaixo de 60% (prioridade) OU passou tempo suficiente
        fuel_priority = self.car.fuel < 60  # Prioridade quando combustível baixo
        
        should_spawn_fuel = (
            current_time - self.last_fuel_spawn > self.fuel_spawn_cooldown and
            (len(self.fuel_pickups) == 0 or self.fuel_pickups[-1].rect.y > 250)
        )
        
        # Se combustível está baixo, reduz o cooldown necessário
        if fuel_priority and current_time - self.last_fuel_spawn > (self.fuel_spawn_cooldown * 0.6):
            should_spawn_fuel = True
        
        if should_spawn_fuel:
            self._spawn_fuel_pickup()
            self.last_fuel_spawn = current_time

        # Spawn de ghost - menos frequente que fuel
        if (
            current_time - self.last_pickup_spawn > self.pickup_cooldown * 1.5
            and random.random() < 0.003
            and (len(self.ghost_pickups) == 0 or self.ghost_pickups[-1].rect.y > 250)
        ):
            self._spawn_ghost_pickup()
            self.last_pickup_spawn = current_time

        # Atualiza fuel pickups
        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if fuel.check_collision(self.car):
                if hasattr(self, "game_manager"):
                    self.game_manager.fuel_pickup_sound.play()
                self.car.fuel = min(self.car.max_fuel, self.car.fuel + 25)  # Aumentado de 20 para 25
                self.fuel_pickups.remove(fuel)
            elif fuel.off_screen(self.height):
                self.fuel_pickups.remove(fuel)

        # Atualiza ghost pickups
        for ghost in self.ghost_pickups[:]:
            ghost.update()
            if ghost.check_collision(self.car):
                if hasattr(self, "game_manager"):
                    self.game_manager.ghost_pickup_sound.play()
                current_time = pygame.time.get_ticks()
                self.car.activate_ghost_power(current_time)   # <-- ATIVA o poder
                self.ghost_pickups.remove(ghost)
            elif ghost.off_screen(self.height):
                self.ghost_pickups.remove(ghost)


        # Spawn da bazuca
        if (
            random.random() < 0.001
            and len([p for p in self.pickups if isinstance(p, RocketPickup)]) == 0
        ):
            lane = random.choice(self.road_lanes)
            self.pickups.append(
                RocketPickup(self.img_config.rocket_pickup_img, lane, self.height)
            )

        # Atualiza rocket pickups
        for pickup in self.pickups[:]:
            pickup.update()
            if pickup.off_screen(self.height):
                self.pickups.remove(pickup)
            elif pickup.check_collision(self.car):
                if isinstance(pickup, RocketPickup):
                    if hasattr(self, "game_manager"):
                        self.game_manager.rocket_pickup_sound.play()
                        self.game_manager.rocket_sound.play()
                    current_time = pygame.time.get_ticks()
                    self.car.activate_rocket_power(current_time)
                self.pickups.remove(pickup)

    def _spawn_fuel_pickup(self):
        """Spawn de fuel pickup com lógica melhorada para facilitar coleta"""
        available_lanes = self.enemy_lanes.copy()

        # Verificação suave - permite spawn mesmo com objetos próximos
        for obj in self.enemies + self.fuel_pickups + self.ghost_pickups:
            if obj.rect.y < 100 and obj.rect.x in available_lanes:  # Mais permissivo
                available_lanes.remove(obj.rect.x)

        # Se não há faixas disponíveis, força o spawn em uma faixa aleatória
        # (garante que sempre terá fuel disponível)
        if not available_lanes:
            available_lanes = self.enemy_lanes.copy()

        lane = random.choice(available_lanes)
        self.fuel_pickups.append(
            FuelPickup(self.img_config.fuel_img, lane, self.height)
        )

    def _spawn_ghost_pickup(self):
        available_lanes = self.road_lanes.copy()

        # Verificação ainda mais rigorosa para ghost pickups
        for obj in self.enemies + self.fuel_pickups + self.ghost_pickups:
            if obj.rect.y < 350 and obj.rect.x in available_lanes:
                available_lanes.remove(obj.rect.x)

        if available_lanes:
            lane = random.choice(available_lanes)
            self.ghost_pickups.append(
                GhostPickup(self.img_config.ghost_power_img, lane, self.height)
            )

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
        
        # Textos flutuantes por último (sempre visíveis)
        for text in self.floating_texts:
            text.draw(surface)
