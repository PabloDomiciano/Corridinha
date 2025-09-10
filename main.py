from config.constants import WIDTH, HEIGHT, TITLE
from core.game_manager import GameManager

if __name__ == "__main__":
    game = GameManager(WIDTH, HEIGHT, TITLE)
    game.run() 