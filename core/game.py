import pygame
import random

# Imports das entidades
from entities.car import Car
from entities.enemy_car import EnemyCar
from entities.fuel import FuelPickup
from entities.track import Track
# Corrigido para refletir o caminho correto do arquivo
from projectile import Projectile
# Descomentar e corrigir a importação do Explosion se necessário
# from explosion import Explosion  # Se você usar a classe Explosion, descomente esta linha

# Imports de UI
from ui.hud import HUD
from ui.screen import Screen

# Configuração das imagens
# Certifique-se de que o caminho está correto
from img.img_config import ImgConfig


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, img, height):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        # As faixas onde o poder pode aparecer
        self.rect.x = random.choice([120, 280])
        self.rect.y = -self.rect.height  # Inicia fora da tela
        self.speed = 5  # Velocidade do poder de atirar

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 640:  # Se sair da tela, remove
            self.kill()


class Game:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = Screen(width, height, title)
        self.projectiles = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()  # Grupo de power-ups

        # Controle de spawn de inimigos e power-ups
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

        # Imagens dos inimigos e power-up
        self.enemy_imgs = [
            self.img_config.ambulancia_img,
            self.img_config.onibus_img,
            self.img_config.car_enemy
        ]
        # Imagem do power-up (poder de atirar)
        self.power_up_img = self.img_config.power_up_img

        # Adiciona uma flag para saber se o jogador pode atirar
        self.can_shoot = False  # Inicialmente, o jogador não pode atirar

    def run(self):
        while self.running:
            self.projectiles.update()
            self.clock.tick(self.fps)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.can_shoot:
                        # Criar novo projétil se o jogador coletou o poder
                        projectile = Projectile(
                            self.car.rect.centerx, self.car.rect.top)
                        self.projectiles.add(projectile)

            self.update(keys)
            self.draw()
            pygame.display.flip()

    def update(self, keys):
        self.track.update()
        self.car.update(keys)
        self.projectiles.update()

        # Spawn controlado de inimigos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.spawn_delay = random.randint(600, 1500)  # delay variável

        # Atualiza inimigos e verifica colisões com os projéteis
        for enemy in self.enemies[:]:
            enemy.update()

            # Ajuste fino do hitbox do inimigo
            inset = 10  # Quanto "encolher" dos lados
            enemy_hitbox = enemy.rect.inflate(-inset, -inset)

            # Verifica a colisão com a hitbox do inimigo
            if self.car.rect.colliderect(enemy_hitbox):
                print("COLISÃO! FIM DE JOGO")
                self.running = False
            if enemy.off_screen():
                self.enemies.remove(enemy)

            # Verifica colisões com projéteis
            for projectile in self.projectiles:
                if projectile.rect.colliderect(enemy.rect):
                    print("INIMIGO DESTRUIDO!")
                    self.enemies.remove(enemy)
                    self.projectiles.remove(projectile)

                    # Criar efeito de explosão
                    # explosion = Explosion(
                    #     enemy.rect.centerx, enemy.rect.centery)
                    # Usando a mesma lista de projéteis para explosão
                    # self.projectiles.add(explosion)

                    # Tocar som de explosão
                    # self.explosion_sound.play()###

        # Atualiza power-ups
        for power_up in self.power_ups:
            power_up.update()
            if self.car.rect.colliderect(power_up.rect):
                print("PODER COLETADO!")
                self.power_ups.remove(power_up)
                self.car.can_shoot = True  # Ativa o poder de tiro

        # Spawn e update de combustível
        if random.random() < 0.01:
            self.fuel_pickups.append(FuelPickup(
                self.img_config.fuel_img, self.height))

        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if self.car.rect.colliderect(fuel.rect):
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
        free_lanes = [lane for lane,
                      in_use in lanes_in_use.items() if not in_use]

        if free_lanes:
            lane = random.choice(free_lanes)
            enemy_img = random.choice(self.enemy_imgs)
            self.enemies.append(EnemyCar(enemy_img, lane, self.height))

    def draw(self):
        self.screen.surface.fill((0, 0, 0))  # limpa a tela
        self.track.draw(self.screen.surface)
        self.projectiles.draw(self.screen.surface)

        for enemy in self.enemies:
            enemy.draw(self.screen.surface)

        for fuel in self.fuel_pickups:
            fuel.draw(self.screen.surface)

        for power_up in self.power_ups:
            power_up.draw(self.screen.surface)

        self.car.draw(self.screen.surface)
        self.hud.update()
        self.hud.draw()

        # Desenha o ícone do poder no canto da tela, se o jogador pode atirar
        if self.can_shoot:
            self.screen.surface.blit(self.img_config.power_up_icon, (10, 10))
