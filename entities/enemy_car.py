from entities.carro import Carro


class EnemyCar(Carro):
    def __init__(self, image, x_pos, screen_height, speed=3):
        super().__init__(image, x_pos, y_pos=-image.get_height(), speed=speed)
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed

    def off_screen(self, height):
        return self.rect.y > height
