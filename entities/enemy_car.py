import random

class EnemyCar:
    def __init__(self, image, x, height):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(-200, -100)
        self.speed = random.randint(4, 7)
        self.height = height

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.top > self.height
