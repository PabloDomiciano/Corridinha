
class BaseEntity:
    def __init__(self, image, x_pos, y_pos):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
