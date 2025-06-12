import pygame
from entities.base import BaseEntity
from entities.hitbox import Hitbox


class Carro(BaseEntity):
    def __init__(self, image, x_pos, y_pos, speed=3):
        super().__init__(image, x_pos, y_pos)
        self.speed = speed
        
        # Estados do carro
        self.is_ghost = False
        self.is_blinking = False
        self.blink_visible = True
        
        # Configurações de visualização
        self.ghost_alpha = 128  # Transparência quando em modo fantasma
        self.blink_interval = 200  # ms entre piscadas
        self.last_blink_time = 0
        
        # Sistema de imagens
        self.normal_image = image.copy()  # Guarda a imagem original
        self.ghost_image = self.create_ghost_image()  # Versão fantasma
        self.blank_image = self.create_blank_image()  # Imagem vazia para piscar
        
        # Inicializa o retângulo e hitbox
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.init_hitbox()

    def create_ghost_image(self):
        """Cria versão semi-transparente do carro."""
        ghost_img = self.normal_image.copy()
        ghost_img.fill((255, 255, 255, self.ghost_alpha), 
                      special_flags=pygame.BLEND_RGBA_MULT)
        return ghost_img

    def create_blank_image(self):
        """Cria uma imagem vazia para o efeito de piscar."""
        blank = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        blank.fill((0, 0, 0, 0))
        return blank

    def init_hitbox(self):
        """Inicializa a hitbox do carro."""
        hitbox_width = self.rect.width 
        hitbox_height = self.rect.height 
        
        hitbox_x = self.rect.x + (self.rect.width - hitbox_width) / 2
        hitbox_y = self.rect.y + (self.rect.height - hitbox_height) / 2

        self.hitbox = Hitbox()
        self.hitbox.set_rect(hitbox_width, hitbox_height, hitbox_x, hitbox_y)

    def set_ghost_mode(self, active, blinking=False):
        """Ativa/desativa modo fantasma e piscar."""
        self.is_ghost = active
        self.is_blinking = blinking
        
        if active:
            self.image = self.ghost_image
        else:
            self.image = self.normal_image
            self.blink_visible = True  # Reseta visibilidade

    def update_blink(self, current_time):
        """Atualiza o estado de piscar."""
        if self.is_blinking and current_time - self.last_blink_time > self.blink_interval:
            self.blink_visible = not self.blink_visible
            self.last_blink_time = current_time
            
            if self.blink_visible:
                self.image = self.ghost_image if self.is_ghost else self.normal_image
            else:
                self.image = self.blank_image

    def update(self):
        """Atualiza o estado do carro."""
        # Atualiza posição da hitbox
        hitbox_x = self.rect.x + (self.rect.width - self.hitbox.rect.width) / 2
        hitbox_y = self.rect.y + (self.rect.height - self.hitbox.rect.height) / 2
        self.hitbox.set_rect(self.hitbox.rect.width, self.hitbox.rect.height, hitbox_x, hitbox_y)

    def draw(self, screen):
        """Desenha o carro na tela."""
        screen.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(screen)

    def check_hitbox_collision(self, other):
        """Verifica colisão entre hitboxes."""
        if self.is_ghost:
            return False
        return self.hitbox.check_rect_collision(other)
    
    def check_collision(self, other_car):
        """Verifica colisão simples com outro carro."""
        if self.is_ghost:
            return False
        return self.rect.colliderect(other_car.rect)