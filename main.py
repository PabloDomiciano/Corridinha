import pygame
import random
import sys
from hud import HUD

# Inicializa o pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 480, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corridinha")

# Clock para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Carrega imagens
track_img = pygame.image.load("./assets/track/track.png").convert()
car_img = pygame.image.load("./assets/cars/car.png").convert_alpha()

# Escala as imagens
enemy_img = pygame.transform.scale(car_img, (60, 100))  # Pode trocar por outro carro futuramente
track_img = pygame.transform.scale(track_img, (WIDTH, HEIGHT))
car_img = pygame.transform.scale(car_img, (60, 100))


# ========== CLASSES ==========

class Track:
    def __init__(self, image):
        self.image = image
        self.y = 0
        self.speed = 5

    def update(self):
        self.y += self.speed
        if self.y >= HEIGHT:
            self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (0, self.y - HEIGHT))
        screen.blit(self.image, (0, self.y))


class Car:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30
        self.speed = 6

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class EnemyCar:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([80, 180, 280, 380])
        self.rect.y = -100
        self.speed = random.randint(4, 7)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT


# ========== INSTÂNCIAS ==========
track = Track(track_img)
car = Car(car_img)
hud = HUD(SCREEN, car)
enemies = []


# ========== LOOP PRINCIPAL ==========
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizações
    track.update()
    car.update(keys)

    # Geração de inimigos
    if random.randint(0, 100) < 2:
        enemies.append(EnemyCar())
# Atualizações de fundo e jogador
    track.update()
    car.update(keys)

    # Geração de inimigos
    if random.randint(0, 100) < 2:
        enemies.append(EnemyCar())

    # Desenho
    track.draw(SCREEN)  # Desenha o fundo primeiro

    for enemy in enemies[:]:  # Depois inimigos
        enemy.update()
        enemy.draw(SCREEN)

        if car.rect.colliderect(enemy.rect):
            print("COLISÃO! FIM DE JOGO")
            running = False

        if enemy.off_screen():
            enemies.remove(enemy)

    car.draw(SCREEN)  # Por último, desenha o carro do jogador
    hud.update()
    hud.draw()

    pygame.display.flip()
pygame.quit()
sys.exit()
