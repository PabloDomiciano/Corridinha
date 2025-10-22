import pygame
from entities.base import BaseEntity
from entities.hitbox import Hitbox


class Carro(BaseEntity):
    """
    Classe intermediária entre BaseEntity e carros jogáveis/inimigos.
    
    Hierarquia de classes:
    BaseEntity -> Carro -> Player (jogador)
                        -> EnemyCar (inimigos)
    
    Responsabilidades:
    - Adicionar velocidade aos objetos
    - Gerenciar hitbox (área de colisão)
    - Fornecer métodos de colisão
    
    Novos atributos além de BaseEntity:
    - speed: Velocidade de movimento
    - hitbox: Área de colisão (pode ser menor que o sprite)
    """
    
    def __init__(self, image, x_pos, y_pos, speed=0):
        """
        Inicializa um carro genérico.
        
        Args:
            image: Imagem do carro
            x_pos, y_pos: Posição inicial
            speed: Velocidade de movimento (pixels por segundo)
        """
        super().__init__(image, x_pos, y_pos)
        self.speed = speed
        
        # Garante que o rect está na posição correta
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        
        # Inicializa a hitbox (área de colisão)
        self.init_hitbox()
    
    def init_hitbox(self):
        """
        Cria a hitbox do carro.
        A hitbox é uma área de colisão que pode ser ajustada
        para ser menor que o sprite visual (mais preciso).
        """
        hitbox_width = self.rect.width
        hitbox_height = self.rect.height
        
        # Centraliza a hitbox no carro
        hitbox_x = self.rect.x + (self.rect.width - hitbox_width) / 2
        hitbox_y = self.rect.y + (self.rect.height - hitbox_height) / 2
        
        self.hitbox = Hitbox()
        self.hitbox.set_rect(hitbox_width, hitbox_height, hitbox_x, hitbox_y)
    
    def update(self):
        """
        Atualiza a hitbox para seguir o carro.
        Chamado pelas classes filhas (Player, EnemyCar).
        """
        if not self.frozen:
            # Recalcula posição da hitbox baseado na posição do carro
            hitbox_x = self.rect.x + (self.rect.width - self.hitbox.rect.width) / 2
            hitbox_y = self.rect.y + (self.rect.height - self.hitbox.rect.height) / 2
            self.hitbox.set_rect(
                self.hitbox.rect.width, 
                self.hitbox.rect.height, 
                hitbox_x, 
                hitbox_y
            )
    
    def draw(self, screen):
        """Desenha o carro e sua hitbox (para debug)"""
        screen.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(screen)
    
    def check_hitbox_collision(self, other):
        """Verifica colisão usando hitboxes (mais preciso)"""
        return self.hitbox.check_rect_collision(other)
    
    def check_collision(self, other_car):
        """Verifica colisão simples usando retângulos"""
        return self.rect.colliderect(other_car.rect)
