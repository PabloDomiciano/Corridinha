from entities.pickup import Pickup

class GhostPickup(Pickup):
    def __init__(self, image, x, screen_height):
        super().__init__(image, x, -image.get_height())
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

    def on_collision(self, car):
        print("Modo fantasma ativado!")
        car.activate_ghost_mode(duration=3000)
