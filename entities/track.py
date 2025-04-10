class Track:
    def __init__(self, image):
        self.image = image
        self.y = 0

    def update(self, speed):
        self.y += speed
        if self.y >= self.image.get_height():
            self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (0, self.y - self.image.get_height()))
        screen.blit(self.image, (0, self.y))
