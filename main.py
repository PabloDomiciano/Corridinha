import pygame
from entities.player import Player
from entities.enemy_car import EnemyCar

# Inicializando o pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Carregar as imagens
player_image = pygame.image.load('assets.cars.car.png')
enemy_image = pygame.image.load('car.png')

# Criando o jogador e o inimigo
player = Player(player_image, screen_width, screen_height, 350, 500)
enemy_car = EnemyCar(enemy_image, 350, screen_height)

# Loop principal do jogo
running = True
while running:
    screen.fill((0, 0, 0))  # Limpa a tela com fundo preto

    # Verificar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar o jogador e o inimigo
    keys = pygame.key.get_pressed()
    player.update(keys)
    enemy_car.update()

    # Desenhar o jogador e o inimigo
    player.draw(screen)
    enemy_car.draw(screen)

    # Atualizar a tela
    pygame.display.flip()

    # Definir a taxa de atualização
    pygame.time.Clock().tick(60)

# Finalizar o pygame
pygame.quit()
