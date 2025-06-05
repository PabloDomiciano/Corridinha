from config.settings import WIDTH, HEIGHT, TITLE
from game_manager import GameManager
import sys
import os

if __name__ == "__main__":
    game = GameManager(WIDTH, HEIGHT, TITLE)
    game.run()
