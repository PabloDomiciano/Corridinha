
from entities.base import BaseEntity
from entities.hitbox import Hitbox


class BasePickup(BaseEntity):
    def __init__(self, image, x_pos, y_pos, speed=5):
        super().__init__(image, x_pos, y_pos)
        self.speed = speed

        # Inicializando a hitbox
        self.hitbox = Hitbox()
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.set_rect(
            self.rect.width,
            self.rect.height,
            self.rect.x,
            self.rect.y
        )

    def update(self):
        """Movimento padrão: desce na tela"""
        self.rect.y += self.speed
        self.update_hitbox()

    def check_collision(self, player):
        """Verifica colisão via hitbox"""
        return self.hitbox.check_rect_collision(player)

    def off_screen(self, screen_height):
        """Se saiu da tela"""
        return self.rect.y > screen_height

    def draw(self, surface):
        super().draw(surface)
        self.hitbox.draw_hitbox(surface)  # Pode remover se não quiser visualizar hitbox
