from core.game import Game
from config.settings import WIDTH, HEIGHT, TITLE

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT, TITLE)
    game.run()
    game.quit()