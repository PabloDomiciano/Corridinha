import pygame
from entities.hitbox import Hitbox


class GhostPowerPickup:
    def __init__(self, image, x_pos, screen_height, ghost_icon):
        # Configurações básicas
        self.image = image
        self.rect = self.image.get_rect(
            topleft=(x_pos, -image.get_height()))  # Começa acima da tela
        self.speed = 5
        self.screen_height = screen_height

        # Configuração da hitbox
        self.hitbox = Hitbox()
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

        # Sistema de HUD e ícone
        self.ghost_icon = ghost_icon
        self.icon_rect = ghost_icon.get_rect(
            bottomleft=(10, screen_height - 10))

        # Controle de tempo e estado
        self.active = False
        self.duration = 10000  # 10 segundos
        self.activation_time = 0
        self.remaining_time = 0

        # Sistema de piscar
        self.blink_start_time = 3000  # Começa a piscar 3s antes do fim
        self.blink_interval = 300  # Intervalo mais rápido para melhor feedback
        self.last_blink_time = 0
        self.visible = True

        # Efeitos visuais
        self.blink_colors = [(0, 255, 0), (255, 255, 0),
                             (255, 165, 0)]  # Verde, Amarelo, Laranja
        self.current_blink_color = 0

    def update(self):
        if not self.active:
            # Movimento normal na tela
            self.rect.y += self.speed
            self.hitbox.set_rect(
                self.rect.width, self.rect.height, self.rect.x, self.rect.y)
        else:
            # Atualiza tempo restante
            current_time = pygame.time.get_ticks()
            self.remaining_time = max(
                0, self.duration - (current_time - self.activation_time))

            # Atualiza efeito de piscar
            if self.remaining_time <= self.blink_start_time:
                if current_time - self.last_blink_time > self.blink_interval:
                    self.visible = not self.visible
                    self.last_blink_time = current_time
                    # Cicla entre cores de alerta
                    self.current_blink_color = (
                        self.current_blink_color + 1) % len(self.blink_colors)

    def activate(self, current_time=None):
        """Ativa o poder com timestamp opcional para sincronização"""
        self.active = True
        self.activation_time = current_time if current_time else pygame.time.get_ticks()
        self.remaining_time = self.duration
        self.visible = True
        self.current_blink_color = 0  # Reseta cor do blink

    def is_active(self):
        """Verifica se o poder está ativo e com tempo restante"""
        return self.active and self.remaining_time > 0

    def get_remaining_time(self):
        """Retorna tempo restante em milissegundos"""
        return self.remaining_time if self.active else 0

    def check_collision(self, player):
        """Verifica colisão com o jogador"""
        return self.hitbox.check_rect_collision(player) if not self.active else False

    def off_screen(self, height):
        """Verifica se saiu da tela"""
        return self.rect.y > height

    def draw(self, surface):
        if not self.active:
            # Desenha o pickup na pista
            surface.blit(self.image, self.rect)
            self.hitbox.draw_hitbox(surface)
        elif self.is_active():
            # Desenha o ícone na HUD (sempre visível, mas com efeitos)
            if self.remaining_time > self.blink_start_time or self.visible:
                surface.blit(self.ghost_icon, self.icon_rect)

            # Barra de progresso com efeito de piscar
            progress = self.remaining_time / self.duration
            bar_width = int(self.icon_rect.width * progress)

            # Muda a cor quando está piscando
            if self.remaining_time <= self.blink_start_time:
                color = self.blink_colors[self.current_blink_color]
            else:
                color = (0, 255, 0)  # Verde

            pygame.draw.rect(surface, color,
                             (self.icon_rect.left, self.icon_rect.top - 5,
                              bar_width, 4))  # Barra mais grossa
