

from entities.car import Car


class EnemyCar(Car):
    def __init__(self, image, lane_x, screen_height):
        # Começa fora da tela (acima do topo)
        super().__init__(image, lane_x, -image.get_height())
        self.speed = 6
        self.screen_height = screen_height

    def update(self, keys=None):
        self.rect.y += self.speed
        # Quando o inimigo sair da tela, reposiciona ele acima da tela
        if self.rect.top > self.screen_height:
            self.rect.y = -self.image.get_height()
