import pygame
from entities.pickups.base_pickup import BasePickup
from entities.pickups.effects.ghost_effect import GhostPickupEffect


class GhostPickup(BasePickup):
    def __init__(self, image, x_pos, y_pos, speed=5, ghost_duration=3000, blink_duration=1000):
        """
        Inicializa um pickup que concede efeito fantasma quando coletado.
        
        Args:
            image: Imagem do pickup
            x_pos: Posição X inicial
            y_pos: Posição Y inicial
            speed: Velocidade de queda
            ghost_duration: Duração do efeito fantasma em ms
            blink_duration: Duração do piscar antes do efeito acabar em ms
        """
        super().__init__(image, x_pos, y_pos, speed)
        
        # Configurações do efeito
        self.ghost_duration = ghost_duration
        self.blink_duration = blink_duration
        
        # Estado do pickup
        self.is_active = True
        self.collected_time = 0
        
        # Efeito fantasma (será aplicado ao jogador quando coletado)
        self.effect = None

    def apply_effect(self, player):
        """Aplica o efeito fantasma ao jogador quando coletado."""
        if not self.is_active:
            return
            
        self.is_active = False
        self.collected_time = pygame.time.get_ticks()
        
        # Cria e configura o efeito no jogador
        self.effect = GhostPickupEffect(player)
        self.effect.set_ghost_mode(active=True)
        
        # Agenda o início do piscar (quando faltar blink_duration ms para acabar)
        blink_start_time = self.ghost_duration - self.blink_duration
        
        # Usamos um evento personalizado para iniciar o piscar no momento certo
        pygame.time.set_timer(pygame.USEREVENT + 1, blink_start_time, loops=1)

    def update_effect(self, current_time):
        """Atualiza o estado do efeito, se estiver ativo."""
        if not self.effect or not self.is_effect_active(current_time):
            return
            
        # Verifica se é hora de começar a piscar
        elapsed = current_time - self.collected_time
        if elapsed > (self.ghost_duration - self.blink_duration):
            self.effect.set_ghost_mode(active=True, blinking=True)
            
        # Atualiza o piscar
        self.effect.update_blink(current_time)
        
        # Verifica se o efeito acabou
        if elapsed >= self.ghost_duration:
            self.remove_effect()

    def is_effect_active(self, current_time):
        """Verifica se o efeito ainda está ativo."""
        if not self.effect or not self.collected_time:
            return False
        return (current_time - self.collected_time) < self.ghost_duration

    def remove_effect(self):
        """Remove completamente o efeito do jogador."""
        if self.effect:
            self.effect.set_ghost_mode(active=False)
            self.effect = None

    def update(self):
        """Atualiza o estado do pickup."""
        if self.is_active:
            super().update()
        else:
            self.update_effect(pygame.time.get_ticks())

    def draw(self, surface):
        """Desenha o pickup (somente se ainda estiver ativo)."""
        if self.is_active:
            super().draw(surface)

    def handle_event(self, event):
        """Lida com eventos (usado para iniciar o piscar no momento certo)."""
        if event.type == pygame.USEREVENT + 1 and self.effect:
            self.effect.set_ghost_mode(active=True, blinking=True)