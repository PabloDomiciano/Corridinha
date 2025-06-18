import pygame


class GhostPickupEffect:
    def __init__(self, entity):
        """
        Efeito de pickup fantasma que pode ser aplicado a qualquer entidade com:
        - image (Surface)
        - rect (Rect)
        - hitbox (Hitbox) [opcional]
        
        Args:
            entity: Referência à entidade que receberá o efeito (ex: Player)
        """
        self.entity = entity

        # Estados do efeito
        self.is_ghost = False
        self.is_blinking = False
        self.blink_visible = True  # Estado atual do piscar

        # Temporizadores
        self.blink_interval = 200  # ms entre piscadas
        self.last_blink_time = 0

        # Configurações visuais
        self.ghost_alpha = 128  # Transparência do modo fantasma (0-255)

        # Backup das imagens originais
        self.normal_image = entity.image.copy()
        self.ghost_image = self._create_ghost_image()
        self.blank_image = self._create_blank_image()

    def _create_ghost_image(self):
        """Cria versão fantasma (semi-transparente) da imagem original."""
        ghost_img = self.normal_image.copy()
        ghost_img.fill((255, 255, 255, self.ghost_alpha), special_flags=pygame.BLEND_RGBA_MULT)
        return ghost_img

    def _create_blank_image(self):
        """Cria imagem totalmente transparente para o piscar."""
        blank = pygame.Surface((self.entity.rect.width, self.entity.rect.height), pygame.SRCALPHA)
        blank.fill((0, 0, 0, 0))
        return blank

    def set_ghost_mode(self, active, blinking=False):
        """
        Ativa/desativa o modo fantasma e piscar.
        
        Args:
            active: True para ativar efeito fantasma
            blinking: True para ativar piscar (normalmente usado no final do efeito)
        """
        self.is_ghost = active
        self.is_blinking = blinking
        self.blink_visible = True  # Reseta estado do piscar

        if active:
            self.entity.image = self.ghost_image
        else:
            self.entity.image = self.normal_image

    def update_blink(self, current_time):
        """Atualiza o estado do piscar baseado no tempo atual."""
        if not self.is_blinking:
            return

        # Troca visibilidade no intervalo definido
        if current_time - self.last_blink_time > self.blink_interval:
            self.blink_visible = not self.blink_visible
            self.last_blink_time = current_time

            # Aplica imagem conforme estado
            if self.blink_visible:
                self.entity.image = self.ghost_image if self.is_ghost else self.normal_image
            else:
                self.entity.image = self.blank_image

    def check_hitbox_collision(self, other):
        """
        Verifica colisão por hitbox, ignorando se estiver em modo fantasma.
        Retorna:
            True se houve colisão e não está no modo fantasma
        """
        if self.is_ghost:
            return False
            
        # Se a entidade tem hitbox, usa ela
        if hasattr(self.entity, 'hitbox'):
            return self.entity.hitbox.check_rect_collision(other)
            
        # Fallback para colisão simples
        return self.entity.rect.colliderect(other.rect)

    def check_collision(self, other):
        """
        Verifica colisão simples (rect), ignorando se estiver em modo fantasma.
        Retorna:
            True se houve colisão e não está no modo fantasma
        """
        if self.is_ghost:
            return False
        return self.entity.rect.colliderect(other.rect)