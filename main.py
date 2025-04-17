import pygame
import random
import sys
from entities.car import Car


from hud import HUD

# Inicializa o pygame
pygame.init()

# Clock para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Carrega imagens
track_img = pygame.image.load("./assets/track/track.png").convert()
car_img = pygame.image.load("./assets/cars/car.png").convert_alpha()
fuel_img = pygame.image.load("./assets/icons/fuel.png").convert_alpha()
enemy_imgs = [
    pygame.image.load("./assets/cars/ambulancia.png").convert_alpha(),
    pygame.image.load("./assets/cars/onibus.png").convert_alpha(),
    pygame.image.load("./assets/cars/car.png").convert_alpha(),
]

# Escala as imagens
# Pode trocar por outro carro futuramente
enemy_img = pygame.transform.scale(car_img, (120, 200))
track_img = pygame.transform.scale(track_img, (WIDTH, HEIGHT))
fuel_img = pygame.transform.scale(fuel_img, (120, 200))


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


class FuelPickup:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([100, 250])
        # Coloca o ícone fora da tela, no topo
        self.rect.y = random.randint(-200, -50)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > HEIGHT




# ========== INSTÂNCIAS ==========

track = Track(track_img)
car = Car()
hud = HUD(SCREEN, car)
enemies = []
fuel_pickups = []


# ========== LOOP PRINCIPAL ==========

running = True
enemy_timer = 0  # Contador de tempo para inimigos
enemy_spawn_rate = 60  # Taxa de spawn dos inimigos (em frames)

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

    # Geração de inimigos (com intervalo de tempo)
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_rate:
        enemies.append(EnemyCar())
        enemy_timer = 0  # Resetando o contador de tempo para o próximo inimigo
        # Intervalo de tempo aleatório entre os inimigos
        enemy_spawn_rate = random.randint(150, 300)

    # Desenho dos inimigos
    for enemy in enemies[:]:
        enemy.update()
        enemy.draw(SCREEN)

        if car.rect.colliderect(enemy.rect):
            print("COLISÃO! FIM DE JOGO")
            running = False

        if enemy.off_screen():
            enemies.remove(enemy)

    # Geração de ícones de combustível (com chance aleatória)
    if random.random() < 0.01:  # 1% de chance de gerar um ícone de combustível a cada frame
        fuel_pickups.append(FuelPickup(fuel_img))

    # Atualizar e desenhar ícones de combustível
    for fuel in fuel_pickups[:]:
        fuel.update()
        fuel.draw(SCREEN)

        # Colisão entre o carro e o ícone de combustível
        if car.rect.colliderect(fuel.rect):
            print("COMBUSTÍVEL RECARREGADO!")
            # Recarrega 20 de combustível
            hud.fuel = min(hud.max_fuel, hud.fuel + 20)
            fuel_pickups.remove(fuel)  # Remove o ícone depois de ser coletado

        if fuel.off_screen():
            fuel_pickups.remove(fuel)

    # Desenho
    track.draw(SCREEN)
    for enemy in enemies:
        enemy.draw(SCREEN)
    car.draw(SCREEN)
    hud.update()
    hud.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
