from core.game_manager import GameManager  
from config.settings import WIDTH, HEIGHT, TITLE

if __name__ == "__main__":
    game = GameManager(WIDTH, HEIGHT, TITLE)  
    game.run()
