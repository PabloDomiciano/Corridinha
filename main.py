import pygame
import sys
from core.game import Game

# Inicializa o pygame
pygame.init()

# Cria a instância principal do jogo
game = Game(width=480, height=640, title="Corridinha")

# Executa o loop do jogo
game.run()

# Finaliza o pygame
pygame.quit()
sys.e
